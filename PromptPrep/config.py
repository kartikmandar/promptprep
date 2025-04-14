"""Handles configuration settings for PromptPrep.

Makes it easy to save your preferred settings and load them later.
"""

import json
import os
import argparse
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Lets you save and load your PromptPrep settings."""

    DEFAULT_CONFIG_DIR = os.path.join(str(Path.home()), ".promptprep")
    DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_DIR, "config.json")

    @classmethod
    def ensure_config_dir(cls) -> None:
        """Creates the config directory if it doesn't exist yet."""
        os.makedirs(cls.DEFAULT_CONFIG_DIR, exist_ok=True)

    @classmethod
    def save_config(
        cls, args: argparse.Namespace, config_file: Optional[str] = None
    ) -> str:
        """Saves your current settings to a file for later use.

        Args:
            args: Your command-line arguments
            config_file: Where to save the config. Uses ~/.promptprep/config.json if not specified

        Returns:
            The path where your config was saved
        """
        if config_file is None:
            config_file = cls.DEFAULT_CONFIG_FILE
            cls.ensure_config_dir()

        config_dict = cls._args_to_dict(args)

        with open(config_file, "w") as f:
            json.dump(config_dict, f, indent=2)

        return config_file

    @classmethod
    def load_config(cls, config_file: Optional[str] = None) -> Dict[str, Any]:
        """Loads your saved settings from a file.

        Args:
            config_file: Where to load from. Uses ~/.promptprep/config.json if not specified

        Returns:
            Your saved settings as a dictionary

        Raises:
            FileNotFoundError: When the config file doesn't exist
        """
        if config_file is None:
            config_file = cls.DEFAULT_CONFIG_FILE

        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

        with open(config_file, "r") as f:
            return json.load(f)

    @staticmethod
    def _args_to_dict(args: argparse.Namespace) -> Dict[str, Any]:
        """Converts command-line arguments to a saveable format.

        Args:
            args: Your command-line arguments

        Returns:
            A dictionary version of your settings
        """
        config_dict = vars(args).copy()

        # Remove non-saveable items
        if "func" in config_dict:
            del config_dict["func"]

        return config_dict

    @staticmethod
    def apply_config_to_args(
        config_dict: Dict[str, Any], args: argparse.Namespace
    ) -> argparse.Namespace:
        """Updates your current settings with values from a config file.

        Args:
            config_dict: Settings loaded from your config file
            args: Your current command-line arguments

        Returns:
            Your updated settings
        """
        args_dict = vars(args)

        # Don't override config file arguments
        for key, value in config_dict.items():
            if key in ["save_config", "load_config"]:
                continue

            if key in args_dict:
                args_dict[key] = value

        return args
