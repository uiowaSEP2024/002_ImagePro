from pathlib import Path
from typing import List, Dict

from trackerapi.schemas import JobConfigs, JobConfig
import json


def load_job_configurations_from_json(filepath: str):
    with open(filepath, "r") as f:
        data = json.load(f)
        return JobConfigs(**data)


def load_job_configuration_from_json(filepath: str):
    with open(filepath, "r") as f:
        data = json.load(f)
        return JobConfig(**data)


class DuplicateJobConfigException(Exception):
    pass


class MissingJobConfigException(Exception):
    pass


class JobConfigManager:
    """
    Helper class for managing job configurations.
    """

    def __init__(self, configs: List[JobConfig] = None, configurations_file: Path | str = None):
        self.config_dict: Dict[str, JobConfig] = {}
        self.init_from_job_configs(configs) if configs else None
        self.init_from_bulk_job_config_json(configurations_file) if configurations_file else None

    def add_job_config(self, config: JobConfig, allow_override=False):
        """
        Adds a job config to the job config dictionary.
        :param config: The job configuration to add to the dictionary
        :param allow_override: Allow replacing an existing job config with same tag as config
        """
        has_existing = self.config_dict.get(config.tag, None)
        if has_existing and not allow_override:
            raise DuplicateJobConfigException(f'Attempting to add config with already existing tag: {config.tag}')
        self.config_dict[config.tag] = config

    def init_from_bulk_job_config_json(self, filepath: Path | str):
        """
        Initializes the job config dictionary from the filepath to a json configuration
        :param filepath:
        """
        bulk_config = load_job_configurations_from_json(filepath)
        self.init_from_job_configs(bulk_config.job_configs)

    def init_from_job_configs(self, configs: List[JobConfig]):
        """
        Adds all job configurations from the list of provided JobConfig's to the dictionary
        :param configs:
        """
        for config in configs:
            self.add_job_config(config)

    @property
    def tags(self):
        """
        :return: List of tags for job configuration dictionary
        """
        return list(self.config_dict.keys())

    def get_job_config(self, tag: str):
        """
        Gets a single job config given its tag
        :param tag: The tag for a job that has been added to the dictionary
        :raise Exception: if no job configuration exists for the given tag
        """
        result = self.config_dict.get(tag, None)
        if result:
            return result

        raise MissingJobConfigException(f"No config with tag: '{tag}'. "
                                        f"Available job configs are: {', '.join(self.tags)}")
