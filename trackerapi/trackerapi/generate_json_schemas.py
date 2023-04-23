import json
from pathlib import Path
from typing import Type
from pydantic import BaseModel
from trackerapi.schemas import JobConfigs
import argparse


def generate_model_json_schema(model: Type[BaseModel], filename: str, location: str = "."):
    json_schema = json.loads(model.schema_json())
    Path(location).mkdir(parents=True, exist_ok=True)
    with open(f"{location}/{filename}.generated.json", "w") as f:
        json.dump(json_schema, f, indent=2)


def generate_job_configs_json_schema(location: str = "./", filename: str = "job-configurations-schema", ):
    generate_model_json_schema(JobConfigs, filename, location)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("location", help="Location of generated schemas")

    args = parser.parse_args()

    generate_job_configs_json_schema(location=args.location)


if __name__ == "__main__":
    main()
