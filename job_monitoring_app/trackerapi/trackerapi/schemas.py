from typing import List, Optional

from pydantic import BaseModel, StrictInt, StrictStr, conlist
from enum import Enum


class UniqueTagModel(BaseModel):
    tag: StrictStr

    def __hash__(self):
        return self.tag

    def __eq__(self, other):
        return self.tag == other.tag


class MetadataKindEnum(str, Enum):
    text = "text"
    number = "number"
    link = "link"


class MetadataConfig(BaseModel):
    name: StrictStr
    kind: MetadataKindEnum = MetadataKindEnum.text
    units: Optional[StrictStr]


class StepConfig(UniqueTagModel):
    points: StrictInt
    name: StrictStr

    metadata_configurations: Optional[List[MetadataConfig]] = []

    def __init__(
        self,
        name: str,
        tag: str,
        points: int,
        metadata_configurations: List[MetadataConfig] = None,
        **kwargs
    ):
        metadata_configurations = (
            metadata_configurations if metadata_configurations else []
        )
        super().__init__(
            name=name,
            tag=tag,
            points=points,
            metadata_configurations=metadata_configurations,
            **kwargs
        )


class StudyConfig(UniqueTagModel):
    name: StrictStr
    step_configurations: conlist(StepConfig, unique_items=True)
    version: str

    def __init__(
        self,
        name: str,
        tag: str,
        step_configurations: List[StepConfig],
        version: str,
        **kwargs
    ):
        super().__init__(
            name=name,
            tag=tag,
            step_configurations=step_configurations,
            version=version,
            **kwargs
        )


class StudyConfigs(BaseModel):
    study_configs: conlist(StudyConfig, unique_items=True)

    def __init__(self, study_configs: List[StudyConfig], **kwargs):
        super().__init__(study_configs=study_configs, **kwargs)
