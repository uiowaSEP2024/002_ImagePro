from semver import Version


class PydanticVersion(Version):
    @classmethod
    def _parse(cls, version):
        return cls.parse(version)

    @classmethod
    def __get_validators__(cls):
        """Return a list of validator methods for pydantic models."""
        yield cls._parse

    @classmethod
    def __modify_schema__(cls, field_schema):
        """Inject/mutate the pydantic field schema in-place."""
        field_schema.update(
            examples=[
                "1.0.2",
                "2.15.3-alpha",
                "21.3.15-beta+12345",
            ]
        )
