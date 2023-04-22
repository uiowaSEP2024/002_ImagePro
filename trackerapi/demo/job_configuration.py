import sys
from pathlib import Path

path_root = Path(__file__).parents[1]
sys.path.append(f"{path_root}/trackerapi")

from trackerapi.trackerapi import TrackerApi
from trackerapi.trackerapi.trackerapiconfig import JobConfig, StepConfig

kidney_scan = StepConfig(name="Kidney Scan", tag="kidney_scan", points=10)
lung_scan: StepConfig(name="Lung Scan", tag="lung_scan", points=20)
xray_drain: StepConfig(name="XRay Drain", tag="xray_drain", points=30)


prostate_v1_config = JobConfig(
    name="Prostate Job",
    tag="prostate_v1_job",
    steps=[kidney_scan, lung_scan, xray_drain],
)

lung_v1_config = JobConfig(
    name="Lung Job", tag="lung_job", steps=[lung_scan, xray_drain]
)
