"""Unit tests for the configuration management functionality."""

import os
import tempfile
import argparse
from unittest import mock
import pytest
from promptprep.config import ConfigManager


def test_args_to_dict():
    """Makes sure we can convert command arguments to a saveable format."""
    # Create a sample namespace with various argument types
    args = argparse.Namespace(
        directory="/test/dir",
        output_file="output.txt",
        include_files="file1.py,file2.py",
        extensions=".py,.js",
        exclude_dirs="node_modules,venv",
        max_file_size=50.0,
        interactive=False,
        summary_mode=True,
        include_comments=True,
        metadata=False,
        count_tokens=True,
        token_model="cl100k_base",
        format="markdown",
        line_numbers=True,
        save_config=None,
        load_config=None,
    )

    # Convert to dictionary
    config_dict = ConfigManager._args_to_dict(args)

    # Check conversion
    assert config_dict["directory"] == "/test/dir"
    assert config_dict["output_file"] == "output.txt"
    assert config_dict["include_files"] == "file1.py,file2.py"
    assert config_dict["extensions"] == ".py,.js"
    assert config_dict["exclude_dirs"] == "node_modules,venv"
    assert config_dict["max_file_size"] == 50.0
    assert config_dict["interactive"] is False
    assert config_dict["summary_mode"] is True
    assert config_dict["include_comments"] is True
    assert config_dict["metadata"] is False
    assert config_dict["count_tokens"] is True
    assert config_dict["token_model"] == "cl100k_base"
    assert config_dict["format"] == "markdown"
    assert config_dict["line_numbers"] is True
    assert config_dict["save_config"] is None
    assert config_dict["load_config"] is None


def test_save_and_load_config():
    """Verifies we can save and reload our settings correctly."""
    # Create a temporary directory for the test
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a config file path
        config_file = os.path.join(temp_dir, "test_config.json")

        # Create sample arguments
        args = argparse.Namespace(
            directory="/test/dir",
            output_file="output.txt",
            include_files="file1.py",
            extensions=".py",
            exclude_dirs="node_modules",
            max_file_size=50.0,
            interactive=False,
            summary_mode=True,
            include_comments=True,
            metadata=False,
            count_tokens=False,
            token_model="cl100k_base",
            format="plain",
            line_numbers=False,
            save_config=None,
            load_config=None,
        )

        # Save config
        saved_path = ConfigManager.save_config(args, config_file)
        assert saved_path == config_file
        assert os.path.exists(config_file)

        # Load config
        loaded_config = ConfigManager.load_config(config_file)

        # Check loaded values
        assert loaded_config["directory"] == "/test/dir"
        assert loaded_config["output_file"] == "output.txt"
        assert loaded_config["include_files"] == "file1.py"
        assert loaded_config["extensions"] == ".py"
        assert loaded_config["exclude_dirs"] == "node_modules"
        assert loaded_config["max_file_size"] == 50.0
        assert loaded_config["interactive"] is False
        assert loaded_config["summary_mode"] is True


def test_apply_config_to_args():
    """Checks that we properly apply loaded settings to current arguments."""
    # Create a config dictionary
    config_dict = {
        "directory": "/config/dir",
        "output_file": "config_output.txt",
        "include_files": "from_config.py",
        "extensions": ".py,.js",
        "exclude_dirs": "config_exclude",
        "max_file_size": 75.0,
        "interactive": True,
        "summary_mode": False,
        "include_comments": False,
    }

    # Create args with some different values
    args = argparse.Namespace(
        directory="/cli/dir",
        output_file="cli_output.txt",
        include_files="",
        extensions="",
        exclude_dirs="",
        max_file_size=100.0,
        interactive=False,
        summary_mode=False,
        include_comments=True,
        metadata=False,
        count_tokens=False,
        token_model="cl100k_base",
        format="plain",
        line_numbers=False,
        save_config=None,
        load_config=None,
    )

    # Apply config to args
    updated_args = ConfigManager.apply_config_to_args(config_dict, args)

    # Check the values were updated
    assert updated_args.directory == "/config/dir"
    assert updated_args.output_file == "config_output.txt"
    assert updated_args.include_files == "from_config.py"
    assert updated_args.extensions == ".py,.js"
    assert updated_args.exclude_dirs == "config_exclude"
    assert updated_args.max_file_size == 75.0
    assert updated_args.interactive is True
    assert updated_args.summary_mode is False
    assert updated_args.include_comments is False

    # Check that fields not in config were left untouched
    assert updated_args.metadata is False
    assert updated_args.count_tokens is False
    assert updated_args.token_model == "cl100k_base"
    assert updated_args.format == "plain"
    assert updated_args.line_numbers is False


def test_load_nonexistent_config():
    """Makes sure we handle missing config files appropriately."""
    with pytest.raises(FileNotFoundError):
        ConfigManager.load_config("/path/to/nonexistent/config.json")


def test_default_config_location():
    """Verifies we create and use the default config location correctly."""
    with mock.patch("os.makedirs") as mock_makedirs:
        with mock.patch("os.path.exists", return_value=False):
            with mock.patch("builtins.open", mock.mock_open()):
                with mock.patch("json.dump"):
                    # Create sample arguments
                    args = argparse.Namespace(
                        directory=os.getcwd(), output_file="output.txt"
                    )

                    # Save config to default location
                    ConfigManager.save_config(args)

                    # Check that the directory was created
                    mock_makedirs.assert_called_once_with(
                        ConfigManager.DEFAULT_CONFIG_DIR, exist_ok=True
                    )
