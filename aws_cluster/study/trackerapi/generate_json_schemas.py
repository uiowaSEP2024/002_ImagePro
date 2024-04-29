import argparse
import json
import sys
from pathlib import Path
from typing import List, Type, Union

from pydantic import BaseModel

from .schemas import StudyConfigs


def generate_model_json_schema(
    model: Type[BaseModel], filename: str, location: str = "."
):
    json_schema = json.loads(model.schema_json())
    Path(location).mkdir(parents=True, exist_ok=True)
    filepath = Path(f"{location}/{filename}.generated.json")
    with open(filepath, "w") as f:
        json.dump(json_schema, f, indent=2)
        print(f"Generated JSON Schema for {model.__name__} at {filepath.absolute()}")


def generate_study_configs_json_schema(
    location: Union[Path, str] = None, filename: str = None
):
    location = location if location else "./"
    filename = filename if filename else "study-configurations-schema"
    generate_model_json_schema(StudyConfigs, filename, location)


def parse_args(args: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--location", help="Location of generated schemas")
    parser.add_argument(
        "-n",
        "--name",
        help="Name to use for the generated <name>.generated.json schema file",
    )
    return parser.parse_args(args)


def main():
    parsed_args = parse_args(sys.argv[1:])
    generate_study_configs_json_schema(
        location=parsed_args.location, filename=parsed_args.name
    )


if __name__ == "__main__":
    main()
