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

        self.learning_rate = lr
        self.dice = Dice(average="macro", num_classes=2, ignore_index=0)
        self.loss_function = GeneralizedDiceFocalLoss(to_onehot_y=True, softmax=True)
        self.scaler = torch.cuda.amp.GradScaler()
        self.validation_step_outputs = []

    def forward(self, x):
        return self.model(x)


def brainmask_inference(data, out_dir=None, postfix=None):
    print("\nDATA: ", data)
    model = BrainmaskModel.load_from_checkpoint(
        checkpoint_path=f"/tmp/NeuroPred_Brainmask_model_file/brainmask_gdf_loss_epoch=123-val_dice_epoch=0.97484.ckpt",
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
            out_im = (
                torch.argmax(test_output, dim=1).detach().cpu()
            )  # convert from one hot encoding
        # out_im = out_im * item["brainmask"]
        item["inferred_label"] = out_im
        item["inferred_label_meta_dict"] = item["image_meta_dict"]

        out_transforms = Compose(
            [
                KeepLargestConnectedComponentd(keys=["inferred_label"]),
                FillHolesd(keys=["inferred_label"]),
                ToITKImaged(keys=["inferred_label"]),
                ResampleMaskToOgd(keys=["inferred_label", "og_image"]),
                SaveITKImaged(
                    keys=["inferred_label"], out_dir=out_dir, output_postfix=postfix
                ),
            ]
        )
        out_transforms(item)

