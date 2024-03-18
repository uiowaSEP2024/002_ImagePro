import os
from pathlib import Path

from ..trackerapi.generate_json_schemas import (
    generate_study_configs_json_schema,
    parse_args,
)


def test_parse_args():
    parsed_args = parse_args(["-l", "hello"])
    assert parsed_args.location == "hello"

    parsed_args = parse_args(["-n", "my-config-schema"])
    assert parsed_args.name == "my-config-schema"


def test_generate_study_configs_json_schema():
    file_dir = os.path.dirname(os.path.realpath(__file__))
    out_dir = Path(file_dir, ".testout")

    expected_schema_path = Path(out_dir, "test-schema.generated.json")

    # Ensure file is not already present
    os.remove(expected_schema_path) if Path.exists(expected_schema_path) else None

    generate_study_configs_json_schema(location=out_dir, filename="test-schema")

    assert Path.exists(
        expected_schema_path
    ), f"Expected file ({expected_schema_path}) to be generated"
    os.remove(expected_schema_path)
