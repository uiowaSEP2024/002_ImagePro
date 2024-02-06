from cnn_transforms import *
import pytorch_lightning as pl
from monai.data import CacheDataset

from monai.networks.layers import Norm
from monai.networks.nets import UNet
from monai.transforms import (
    Compose,
    ScaleIntensityRangePercentilesd,
    ToTensord,
    CopyItemsd,
    KeepLargestConnectedComponentd,
    FillHolesd
)
from torchmetrics.classification import Dice
import torch
from monai.losses.dice import GeneralizedDiceFocalLoss

itk.MultiThreaderBase.SetGlobalDefaultNumberOfThreads(1)

from pathlib import Path
from dcm_classifier.study_processing import ProcessOneDicomStudyToVolumesMappingBase
from dcm_classifier.image_type_inference import ImageTypeClassifierBase
from dcm_classifier.namic_dicom_typing import itk_read_from_dicomfn_list
import re
from pydicom import dcmread
from subprocess import run


def validate_subject_id(subject_id: str) -> str:
    if "sub-" in subject_id:
        return subject_id
    else:
        return f"sub-{subject_id}"


def validate_session_id(session_id: str) -> str:
    if "ses-" in session_id:
        return session_id
    else:
        return f"ses-{session_id}"


def dicom_inference_and_conversion(
    session_dir: str, output_dir: str, model_path: str
) -> str:
    """
    This function takes a session directory with dicom data and converts them to NIfTI files in BIDS format.
    :param session_dir: path to the session directory with dicom data
    :param output_dir: path to the output directory (base NIfTI directory)
    :param model_path: path to the model used for image type inference
    :param dcm2niix_path_path: path to the dcm2niix script
    :return: path to the NIfTI sub-*/ses-* directory with converted data
    """
    inferer = ImageTypeClassifierBase(
        classification_model_filename=model_path, min_probability_threshold=0.2
    )
    study = ProcessOneDicomStudyToVolumesMappingBase(
        study_directory=session_dir, inferer=inferer
    )
    study.run_inference()
    sub, ses, sub_ses_dir = None, None, None
    for series_number, series in study.series_dictionary.items():
        dcm_info = dcmread(
            series.volume_info_list[0].one_volume_dcm_filenames[0],
            stop_before_pixels=True,
            force=True,
        )
        sub = re.sub("[\W_]", "", dcm_info["PatientID"].value)
        ses = re.sub("[\W_]", "", dcm_info["AcquisitionDate"].value)
        sub_ses_dir = f"{output_dir}/sub-{sub}/ses-{ses}/raw_nifti"
        if not Path(sub_ses_dir).exists():
            run(["mkdir", "-p", sub_ses_dir])

        plane = series.get_acquisition_plane()
        print("Sub:", sub, "series:", series_number, "plane:", plane)

        modality = series.get_modality()
        if modality != "INVALID":
            if not Path(sub_ses_dir).exists():
                run(["mkdir", "-p", sub_ses_dir])
            fname = f"{validate_subject_id(sub)}_{validate_session_id(ses)}_acq-{plane}_{modality}"
            series_vol_list = series.get_volume_list()
            if len(series_vol_list) > 1:
                print(f"Series {series_number} not supported. More than one volume in series.")
            else:
                itk_im = itk_read_from_dicomfn_list(series_vol_list[0].get_one_volume_dcm_filenames())
                itk.imwrite(itk_im, f"{sub_ses_dir}/{fname}.nii.gz")

    return sub_ses_dir


class BrainmaskModel(pl.LightningModule):
    def __init__(self, lr=0.001):
        super().__init__()
        # initialize network architecture
        self.model = UNet(
            spatial_dims=3,
            in_channels=1,
            out_channels=2,
            channels=(16, 32, 64, 128, 256),
            strides=(2, 2, 2, 2),
            num_res_units=3,
            norm=Norm.BATCH,
        )

    def forward(self, x):
        return self.model(x)


def brainmask_inference(data: list, model_file: str, out_dir: str, postfix='brainmask') -> None:
    print("\nDATA: ", data)
    model = BrainmaskModel.load_from_checkpoint(
        checkpoint_path=model_file,
    )
    # set device, GPU or CPU
    # device = torch.device("cuda:0")
    device = torch.device("cpu")
    model.to(device)

    test_transforms = Compose(
        [
            CopyItemsd(keys=["image"], times=1, names=["og_image"]),
            LoadITKImaged(keys=["image", "og_image"]),
            ResampleStartRegionBrainMaskd(
                keys=[
                    "image",
                ],
                inference=True,
                spacing=[1, 1, 1],
                im_size=[192, 192, 160],
            ),
            ITKImageToNumpyd(keys=["image"]),
            ScaleIntensityRangePercentilesd(
                keys=["image"],
                lower=2.0,
                upper=98.0,
                b_min=-1.0,
                b_max=1.0,
                clip=True,  # false
                relative=False,
            ),
            AddChanneld(keys=["image"]),
            ToTensord(keys=["image"], dtype=torch.float32),
        ]
    )
    test_dataset = CacheDataset(
        data=data, transform=test_transforms, cache_rate=1.0, num_workers=16
    )

    for i in range(len(data)):
        item = test_dataset.__getitem__(
            i
        )  # extract image and label from loaded dataset
        with torch.no_grad():  # perform the inference
            test_output = model.model(item["image"].unsqueeze(dim=0).to(device))
            # convert from one hot encoding
            out_im = (
                torch.argmax(test_output, dim=1).detach().cpu()
            )

        print(out_im.shape)
        item["inferred_label"] = out_im #.squeeze(dim=0)
        item["inferred_label_meta_dict"] = item["image_meta_dict"]
        item["inferred_label_meta_dict"]["filename"] = item["image_meta_dict"][
            "filename"
        ].replace(f"_{item['image_meta_dict']['filename'].split('_')[-1]}", ".nii.gz")

        out_transforms = Compose(
            [
                ToITKImaged(keys=["inferred_label"]),
                ResampleMaskToOgd(keys=["inferred_label", "og_image"]),
                SaveITKImaged(
                    keys=["inferred_label"], out_dir=out_dir, output_postfix=postfix
                ),
            ]
        )
        out_transforms(item)

