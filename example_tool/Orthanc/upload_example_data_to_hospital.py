from pyorthanc import Orthanc
import pydicom
from pathlib import Path


def upload_single_study_dir(orthanc: Orthanc, base_data_path: Path) -> None:
    # study_instance_uid: str | None = None
    for dicom_file in base_data_path.glob("**/*"):
        if dicom_file.is_file():
            try:
                _ = pydicom.dcmread(dicom_file, stop_before_pixels=True)
            except pydicom.errors.InvalidDicomError:
                # Not dicom file
                continue
            with open(dicom_file, "rb") as file:
                print(f"Pushing: {dicom_file}")
                orthanc.post_instances(file.read())


def do_main():
    client_orthanc = Orthanc("http://127.0.0.1:8030")
    file_path = Path(__file__)
    example_tool_path = file_path.parent.parent
    data_path = example_tool_path.parent / "example_data/CAIPIRINHA_SPACE_Neuro_Head_Examples"
    upload_single_study_dir(client_orthanc, data_path)


if __name__ == "__main__":
    do_main()
