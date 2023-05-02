from pydantic import StrictStr, BaseModel


class UniqueTagModel(BaseModel):
    tag: StrictStr

    def __hash__(self):
        return self.tag

    def __eq__(self, other):
        return self.tag == other.tag
