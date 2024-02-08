import itk
import numpy as np
from pathlib import Path
import torch
import re


class LoadITKImaged(object):
    def __init__(self, keys, pixel_type=itk.F, debug=False):
        self.keys = keys
        self.pixel_type = pixel_type
        self.meta_updater = UpdateMetaDatad(keys=self.keys)

    def __call__(self, data):
        d = dict(data)
        for k in self.keys:
            # print(d[k])
            # save off the file name
            if f"{k}_meta_dict" not in d.keys():
                d[f"{k}_meta_dict"] = {"filename": d[k]}
            else:
                d[f"{k}_meta_dict"]["filename"] = d[k]

            if k == "label_96" or k == "label" or k == "mask" or k == "og_image":
                d[k] = itk.imread(d[k], itk.UC)
            else:
                d[k] = itk.imread(d[k], self.pixel_type)

        d = self.meta_updater(d)

        return d


def get_direction_cos_from_image(image):
    dims = len(image.GetOrigin())
    arr = np.array([[0.0] * dims] * dims)
    mat = image.GetDirection().GetVnlMatrix()
    for i in range(dims):
        for j in range(dims):
            arr[i][j] = mat.get(i, j)
    return arr


class UpdateMetaDatad(object):
    def __init__(self, keys):
        self.keys = keys

    def __call__(self, data):
        d = dict(data)
        for k in self.keys:
            image = d[k]
            if f"{k}_meta_dict" not in d.keys():
                d[f"{k}_meta_dict"] = {}
            d[f"{k}_meta_dict"]["origin"] = np.array(image.GetOrigin())
            d[f"{k}_meta_dict"]["spacing"] = np.array(image.GetSpacing())
            d[f"{k}_meta_dict"]["direction"] = get_direction_cos_from_image(image)

        return d


# conversion functions
class ITKImageToNumpyd(object):
    def __init__(self, keys):
        self.keys = keys
        self.meta_updater = UpdateMetaDatad(keys=self.keys)

    def __call__(self, data):
        d = dict(data)
        d = self.meta_updater(d)
        for k in self.keys:
            d[k] = itk.array_from_image(d[k])

        return d


class ToITKImaged(object):
    # TODO: apply changes and test like in the other transform file
    def __init__(self, keys):
        self.keys = keys
        pass

    def __call__(self, data):
        d = dict(data)
        for k in self.keys:
            if torch.is_tensor(d[k]):
                d[k] = d[k].numpy().astype(np.float32)
            if len(d[k].shape) == 5:
                d[k] = d[k].squeeze(axis=0).squeeze(axis=0)
            elif len(d[k].shape) == 4:
                d[k] = d[k].squeeze(axis=0)

            meta_data = d[f"{k}_meta_dict"]
            itk_image = itk.image_from_array(d[k])
            itk_image.SetOrigin(meta_data["origin"])
            itk_image.SetSpacing(meta_data["spacing"])
            itk_image.SetDirection(meta_data["direction"])

            d[k] = itk_image
        return d


def sub_from_path(file_path):
    sub = re.findall("sub-\\w+\\d+", file_path)[0]
    return sub


class SaveITKImaged(object):
    def __init__(
        self, keys, out_dir=None, output_postfix="inf", same_dir=False, overwrite=False
    ):
        self.keys = keys
        self.postfix = output_postfix
        self.out_dir = out_dir
        self.same_dir = same_dir
        self.overwrite = overwrite

    def __call__(self, data):
        d = dict(data)
        for k in self.keys:
            filepath = d[f"{k}_meta_dict"]["filename"]
            fname = Path(filepath).name
            extension = f".{'.'.join(str(fname).split('.')[-2:])}"
            basename = fname.replace(extension, "")
            out_fname = f"{basename}_{self.postfix}{extension}"
            if self.same_dir:
                file_dir = Path(filepath).parent
                output_filename = f"{file_dir}/{out_fname}"
            elif self.overwrite:
                output_filename = filepath
            else:
                output_filename = f"{self.out_dir}/{out_fname}"
            print("writing to", output_filename)
            itk.imwrite(d[k], output_filename)
            pass

        return d


class AddChanneld(object):
    def __init__(self, keys):
        self.keys = keys

    def __call__(self, data):
        d = dict(data)
        for k in self.keys:
            im = d[k]
            im = np.expand_dims(im, axis=0)
            d[k] = im

        return d


# unsqueze_lambda = lambda x: x.squeeze(dim=0)
# shape_lambda = lambda x: x.shape


class ResampleMaskToOgd(object):
    def __init__(self, keys):
        # assert len(keys) == 2, "must pass in a t1w key and label key"
        self.t1w_key = keys[1]
        self.label_key = keys[0]

    def __call__(self, data):
        d = dict(data)
        t1w_itk_image = d[self.t1w_key]
        label_itk_image = d[self.label_key]
        image_type = itk.Image[itk.F, 3]
        label_type = itk.Image[itk.UC, 3]
        castImageFilter = itk.CastImageFilter[image_type, label_type].New()
        castImageFilter.SetInput(label_itk_image)

        nearest_interpolator = itk.NearestNeighborInterpolateImageFunction[
            label_type, itk.D
        ].New()
        identity_transform = itk.IdentityTransform[itk.D, 3].New()

        ref_image = t1w_itk_image
        label_resampler = itk.ResampleImageFilter[label_type, label_type].New()
        label_resampler.SetInterpolator(nearest_interpolator)
        label_resampler.SetTransform(identity_transform)
        label_resampler.SetInput(castImageFilter.GetOutput())
        label_resampler.SetReferenceImage(ref_image)
        label_resampler.UseReferenceImageOn()
        label_resampler.UpdateLargestPossibleRegion()

        # update the dictionary
        d[self.label_key] = label_resampler.GetOutput()
        return d


class ResampleStartRegionBrainMaskd(object):
    def __init__(
        self, keys, spacing, im_size, inference=False, label_pixel_type=itk.UC
    ):
        self.inference = inference
        self.tracew_key = keys[0]
        # self.adc_key = keys[1]
        self.lbl_pix_type = label_pixel_type
        self.spacing = spacing
        self.im_size = im_size
        if not self.inference:
            self.label_key = keys[1]

    def __call__(self, data):
        d = dict(data)
        tracew_itk_image = d[self.tracew_key]
        # adc_itk_image = d[self.adc_key]

        image_type = itk.Image[itk.F, 3]
        linear_interpolator = itk.LinearInterpolateImageFunction[
            image_type, itk.D
        ].New()
        identity_transform = itk.IdentityTransform[itk.D, 3].New()

        center, mask = self.get_image_center(tracew_itk_image)
        # d[f"brainmask"] = mask
        ref_image = self.setup_reference_image(
            self.spacing, self.im_size, center, pixel_type=itk.F
        )
        tracew_resampler = itk.ResampleImageFilter[image_type, image_type].New()
        tracew_resampler.SetInterpolator(linear_interpolator)
        tracew_resampler.SetTransform(identity_transform)
        tracew_resampler.SetInput(tracew_itk_image)
        tracew_resampler.SetReferenceImage(ref_image)
        tracew_resampler.UseReferenceImageOn()
        tracew_resampler.UpdateLargestPossibleRegion()

        d[self.tracew_key] = tracew_resampler.GetOutput()
        # d[self.adc_key] = adc_resampler.GetOutput()

        if not self.inference:
            label_itk_image = d[self.label_key]
            label_type = itk.Image[self.lbl_pix_type, 3]
            nearest_interpolator = itk.NearestNeighborInterpolateImageFunction[
                label_type, itk.D
            ].New()
            # ref_label = self.setup_reference_image(label_itk_image, pixel_type=itk.UC)
            label_resampler = itk.ResampleImageFilter[label_type, label_type].New()
            label_resampler.SetInterpolator(nearest_interpolator)
            label_resampler.SetTransform(identity_transform)
            label_resampler.SetInput(label_itk_image)
            label_resampler.SetReferenceImage(ref_image)
            label_resampler.UseReferenceImageOn()
            label_resampler.UpdateLargestPossibleRegion()

            # update the dictionary

            d[self.label_key] = label_resampler.GetOutput()
        return d

    def get_image_center(self, image):
        arr = itk.GetArrayFromImage(image)
        arr[arr > 0] = 1
        mask = itk.GetImageFromArray(arr)
        mask.CopyInformation(image)

        label_type = itk.Image[itk.UC, 3]
        castImageFilter = itk.CastImageFilter[type(image), label_type].New()
        castImageFilter.SetInput(mask)
        castImageFilter.UpdateLargestPossibleRegion()
        mask = castImageFilter.GetOutput()
        # itk.imwrite(
        #     mask,
        #     "/Shared/johnsonhj/2021Projects/20211221_boeslab_stroke/boes_stroke_characterization/code/CNN/transform_test/mask.nii.gz",
        # )

        moments_calc = itk.ImageMomentsCalculator[type(mask)].New()
        moments_calc.SetImage(mask)
        moments_calc.Compute()
        centroid = moments_calc.GetCenterOfGravity()
        return centroid, mask

    def setup_reference_image(self, spacing, im_size, center, pixel_type):
        im_spacing = spacing

        size = itk.Size[3]()
        size[0] = im_size[0]  # size along X
        size[1] = im_size[1]  # size along Y
        size[2] = im_size[2]  # size along Z

        start = itk.Index[3]()
        start[0] = 0  # first index on Xcd
        start[1] = 0  # first index on Y
        start[2] = 0  # first index on Z

        origin = np.array(center) - (
            np.array([(size[0] / 2 - 1), (size[1] / 2 - 1), (size[2] / 2 - 1)])
            * np.array(im_spacing)
        )
        ImageType = itk.Image[pixel_type, 3]
        fixed_field = ImageType.New()
        fixed_field.SetOrigin(origin.tolist())
        fixed_field.SetSpacing(im_spacing)

        region = itk.ImageRegion[3]()
        region.SetSize(size)
        region.SetIndex(start)

        fixed_field.SetRegions(region)
        fixed_field.Allocate()

        return fixed_field
