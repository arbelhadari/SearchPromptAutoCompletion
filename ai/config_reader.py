import json
from abc import ABC, abstractmethod
from typing import Any


class IConfigReader(ABC):
    """Abstract base class for configuration readers.

    This class defines the interface for configuration readers that can retrieve
    configuration values from different sources.

    Methods:
        get_config_value(path: str, key: str) -> Any:
            Abstract method that must be implemented by subclasses to retrieve a configuration value
            from the specified path using the given key.
    """
    @staticmethod
    @abstractmethod
    def get_config_value(path: str, key: str) -> Any:
        pass


class JSONConfigReader(IConfigReader):
    """Configuration reader for JSON files.

    This class implements the IConfigReader interface to read configuration values from JSON files.

    Methods:
        get_config_value(path: str, key: str) -> Any:
            Retrieves a configuration value from a JSON file at the specified path using the given key.
    """

    @staticmethod
    def get_config_value(path: str, key: str) -> Any:
        """Retrieves a configuration value from a JSON file.

        Args:
            path (str): The path to the JSON configuration file.
            key (str): The key for the desired configuration value.

        Returns:
            Any: The configuration value corresponding to the key, or `None` if the key is not found.
        
        Raises:
            FileNotFoundError: If the file at the specified path does not exist.
            json.JSONDecodeError: If the file at the specified path is not a valid JSON file.
        """
        try:
            with open(path) as config_file:
                config = json.load(config_file)

            return config.get(key, None)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"An error occurred while reading the config file: {e}")
            return None