import json
from pathlib import Path
from typing import Dict, List, Union

from .schemas import StudyConfig, StudyConfigs


def load_study_configurations_from_json(filepath: str):
    with open(filepath, "r") as f:
        data = json.load(f)
        return StudyConfigs(**data)


def load_study_configuration_from_json(filepath: str):
    with open(filepath, "r") as f:
        data = json.load(f)
        return StudyConfig(**data)


class DuplicateStudyConfigException(Exception):
    pass


class MissingStudyConfigException(Exception):
    pass


class StudyConfigManager:
    """
    Helper class for managing study configurations.
    """

    def __init__(
        self,
        configs: List[StudyConfig] = None,
        configurations_file: Union[Path, str] = None,
    ):
        self.config_dict: Dict[str, StudyConfig] = {}
        self.init_from_study_configs(configs) if configs else None
        self.init_from_bulk_study_config_json(
            configurations_file
        ) if configurations_file else None

    def add_study_config(self, config: StudyConfig, allow_override=False):
        """
        Adds a study config to the study config dictionary.
        :param config: The study configuration to add to the dictionary
        :param allow_override: Allow replacing an existing study config with same tag as config
        """
        has_existing = self.config_dict.get(config.tag, None)
        if has_existing and not allow_override:
            raise DuplicateStudyConfigException(
                f"Attempting to add config with already existing tag: {config.tag}"
            )
        self.config_dict[config.tag] = config

    def init_from_bulk_study_config_json(self, filepath: Union[Path, str]):
        """
        Initializes the study config dictionary from the filepath to a json configuration
        :param filepath:
        """
        bulk_config = load_study_configurations_from_json(filepath)
        self.init_from_study_configs(bulk_config.study_configs)

    def init_from_study_configs(self, configs: List[StudyConfig]):
        """
        Adds all study configurations from the list of provided StudyConfig's to the dictionary
        :param configs:
        """
        for config in configs:
            self.add_study_config(config)

    @property
    def tags(self):
        """
        :return: List of tags for study configuration dictionary
        """
        return list(self.config_dict.keys())

    def get_study_config(self, tag: str):
        """
        Gets a single study config given its tag
        :param tag: The tag for a study that has been added to the dictionary
        :raise Exception: if no study configuration exists for the given tag
        """
        result = self.config_dict.get(tag, None)
        if result:
            return result

        raise MissingStudyConfigException(
            f"No config with tag: '{tag}'. "
            f"Available study configs are: {', '.join(self.tags)}"
        )
