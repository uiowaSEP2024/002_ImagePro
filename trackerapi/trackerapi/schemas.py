from abc import ABC, abstractmethod
from typing import List, Dict

from pydantic import BaseModel, StrictInt, StrictStr, conlist


class UniqueTagModel(BaseModel):
    tag: StrictStr

    def __hash__(self):
        return self.tag

    def __eq__(self, other):
        return self.tag == other.tag


class StepConfig(UniqueTagModel):
    points: StrictInt
    name: StrictStr

    def __init__(self, name: str, tag: str, points: int, **kwargs):
        super().__init__(name=name, tag=tag, points=points, **kwargs)


class JobConfig(UniqueTagModel):
    name: StrictStr
    steps: conlist(StepConfig, unique_items=True)

    def __init__(self, name: str, tag: str, steps: List[StepConfig], **kwargs):
        super().__init__(name=name, tag=tag, steps=steps, **kwargs)


class JobConfigs(BaseModel):
    job_configs: conlist(JobConfig, unique_items=True)

    def __init__(self, job_configs: List[JobConfig], **kwargs):
        super().__init__(job_configs=job_configs, **kwargs)
