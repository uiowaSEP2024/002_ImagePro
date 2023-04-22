from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel, StrictInt, StrictStr


class StepConfig(BaseModel):
    tag: StrictStr
    points: StrictInt
    name: StrictStr

    def __init__(self, name: str, tag: str, points: int, **kwargs):
        super().__init__(name=name, tag=tag, points=points, **kwargs)


class JobConfig(BaseModel):
    tag: StrictStr
    name: StrictStr
    steps: List[StepConfig]

    def __init__(self, name: str, tag: str, steps: List[StepConfig], **kwargs):
        super().__init__(name=name, tag=tag, steps=steps, **kwargs)
