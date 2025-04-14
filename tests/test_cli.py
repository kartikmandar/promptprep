import argparse
import os
import sys
import tempfile
import pytest
from unittest import mock
from io import StringIO
import subprocess
import json
from promptprep.cli import parse_arguments, main


def run_script(args, cwd):
    """Helps us test the CLI by running it and capturing what it does."""
    cmd = [
        sys.executable,
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "..", "promptprep", "cli.py"
        ),
    ]
    print(f"Running command: {' '.join(cmd)}")
    print(f"Working directory: {cwd}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    print(f"Exit code: {result.returncode}")
    print(f"Standard output: {result.stdout}")
    print(f"Error output: {result.stderr}")
    return result


def test_parse_arguments():
    """Makes sure we understand all command-line arguments correctly."""
    # Test with no args (default values)
    with mock.patch.object(sys, "argv", ["promptprep"]):
        args = parse_arguments()
        assert args.directory == os.getcwd()
        assert args.output_file == "full_code.txt"
        assert args.clipboard is False

    # Test with directory and output file
    test_dir = "/test/dir"
    test_output = "output.txt"
    with mock.patch.object(
        sys, "argv", ["promptprep", "-d", test_dir, "-o", test_output]
    ):
        args = parse_arguments()
        assert args.directory == test_dir
        assert args.output_file == test_output


def test_main_file_output():
    """Verifies we can write our aggregated code to a file properly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test file
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write("print('hello')")

        # Mock arguments
        args_mock = mock.Mock()
        args_mock.directory = tmpdir
        args_mock.output_file = "test_output.txt"
        args_mock.clipboard = False
        args_mock.include_files = ""
        args_mock.extensions = ""
        args_mock.exclude_dirs = ""
        args_mock.max_file_size = 100.0
        args_mock.interactive = False
        args_mock.summary_mode = False
        args_mock.include_comments = True
        args_mock.metadata = False
        args_mock.count_tokens = False
        args_mock.token_model = "cl100k_base"
        args_mock.format = "plain"
        args_mock.line_numbers = False
        args_mock.load_config = None
        args_mock.template_file = None
        args_mock.save_config = None
        # Add missing attributes
        args_mock.incremental = False
        args_mock.last_run_timestamp = None
        args_mock.prev_file = None  # Add this to prevent the Mock object issue

        # Mock parse_arguments to return our args
        with mock.patch("promptprep.cli.parse_arguments", return_value=args_mock):
            # Capture stdout
            with mock.patch("sys.stdout", new=StringIO()) as fake_out:
                main()
                assert (
                    f"Aggregated file '{args_mock.output_file}' created successfully."
                    in fake_out.getvalue()
                )

                # Check if file was created
                output_path = os.path.join(os.getcwd(), args_mock.output_file)
                assert os.path.exists(output_path)
                os.remove(output_path)  # Clean up


def test_main_with_invalid_directory():
    """Checks that we handle non-existent directories gracefully."""
    invalid_dir = "/invalid/path/that/does/not/exist"
    args_mock = mock.Mock()
    args_mock.directory = invalid_dir
    args_mock.output_file = "test_output.txt"
    args_mock.clipboard = False
    args_mock.include_files = ""
    args_mock.extensions = ""
    args_mock.exclude_dirs = ""
    args_mock.max_file_size = 100.0
    args_mock.interactive = False  # Ensure interactive mode is disabled
    args_mock.summary_mode = False
    args_mock.include_comments = True
    args_mock.metadata = False
    args_mock.count_tokens = False
    args_mock.token_model = "cl100k_base"
    args_mock.format = "plain"
    args_mock.line_numbers = False
    args_mock.load_config = None  # Add missing attribute
    args_mock.template_file = None  # Add missing attribute
    args_mock.save_config = None  # Add missing attribute
    # Add missing attributes
    args_mock.incremental = False
    args_mock.last_run_timestamp = None
    args_mock.prev_file = None

    with (
        mock.patch("promptprep.cli.parse_arguments", return_value=args_mock),
        mock.patch("sys.stderr", new=StringIO()) as fake_err,
        pytest.raises(SystemExit) as excinfo,
    ):
        main()
        assert "Error: Directory not found" in fake_err.getvalue()
        assert excinfo.value.code == 1


def test_parse_arguments_config_options():
    """Makes sure our config-related arguments work as expected."""
    # Test save config (default location)
    with mock.patch.object(sys, "argv", ["promptprep", "--save-config"]):
        args = parse_arguments()
        assert args.save_config == "default"

    # Test save config (custom location)
    custom_location = "/path/to/config.json"
    with mock.patch.object(
        sys, "argv", ["promptprep", "--save-config", custom_location]
    ):
        args = parse_arguments()
        assert args.save_config == custom_location

    # Test load config (default location)
    with mock.patch.object(sys, "argv", ["promptprep", "--load-config"]):
        args = parse_arguments()
        assert args.load_config == "default"

    # Test load config (custom location)
    with mock.patch.object(
        sys, "argv", ["promptprep", "--load-config", custom_location]
    ):
        args = parse_arguments()
        assert args.load_config == custom_location


def test_main_save_config():
    """Verifies we can save our settings to a config file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = os.path.join(temp_dir, "test_config.json")

        # Mock the arguments
        test_args = argparse.Namespace(
            directory=temp_dir,
            output_file="output.txt",
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
            save_config=config_path,
            load_config=None,
            clipboard=False,
            template_file=None,
        )

        # Mock parse_arguments to return our test args
        with mock.patch("promptprep.cli.parse_arguments", return_value=test_args):
            # Mock the save_config method
            with mock.patch(
                "promptprep.config.ConfigManager.save_config", return_value=config_path
            ) as mock_save:
                # Mock sys.argv to simulate only --save-config argument
                with mock.patch.object(
                    sys, "argv", ["promptprep", "--save-config", config_path]
                ):
                    # Capture stdout
                    with mock.patch("sys.stdout", new=StringIO()) as fake_stdout:
                        main()

                        # Check that config was saved
                        mock_save.assert_called_once()

                        # Check output message
                        assert (
                            f"Configuration saved to '{config_path}'"
                            in fake_stdout.getvalue()
                        )

                        # Check that we didn't proceed to file aggregation
                        assert "Aggregated file" not in fake_stdout.getvalue()


def test_main_load_config():
    """Makes sure we can load our saved settings from a config file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test config file
        config_path = os.path.join(temp_dir, "test_config.json")
        test_config = {
            "directory": temp_dir,
            "output_file": "from_config.txt",
            "include_files": "test.py",
            "extensions": ".py,.js",
            "exclude_dirs": "node_modules",
            "max_file_size": 75.0,
            "interactive": False,
            "summary_mode": True,
            "include_comments": False,
            "template_file": None,
        }

        with open(config_path, "w") as f:
            json.dump(test_config, f)

        # Create initial args (before loading config)
        initial_args = argparse.Namespace(
            directory=os.getcwd(),  # Different from config
            output_file="default.txt",  # Different from config
            include_files="",
            extensions="",
            exclude_dirs="",
            max_file_size=100.0,
            interactive=False,
            summary_mode=False,  # Different from config
            include_comments=True,  # Different from config
            metadata=False,
            count_tokens=False,
            token_model="cl100k_base",
            format="plain",
            line_numbers=False,
            save_config=None,
            load_config=config_path,
            clipboard=False,
            template_file=None,
            # Add missing attributes
            incremental=False,
            last_run_timestamp=None,
            prev_file=None,
        )

        # Mock parse_arguments to return initial args
        with mock.patch("promptprep.cli.parse_arguments", return_value=initial_args):
            # Create a merged args object that would result from loading the config
            merged_args = argparse.Namespace(**vars(initial_args))
            merged_args.directory = test_config["directory"]
            merged_args.output_file = test_config["output_file"]
            merged_args.include_files = test_config["include_files"]
            merged_args.extensions = test_config["extensions"]
            merged_args.exclude_dirs = test_config["exclude_dirs"]
            merged_args.max_file_size = test_config["max_file_size"]
            merged_args.summary_mode = test_config["summary_mode"]
            merged_args.include_comments = test_config["include_comments"]

            # Mock the load_config and apply_config methods
            with mock.patch(
                "promptprep.config.ConfigManager.load_config", return_value=test_config
            ):
                with mock.patch(
                    "promptprep.config.ConfigManager.apply_config_to_args",
                    return_value=merged_args,
                ):
                    # Mock CodeAggregator to avoid actual file operations
                    mock_instance = mock.Mock()
                    mock_instance.write_to_file.return_value = None

                    with mock.patch(
                        "promptprep.cli.CodeAggregator", return_value=mock_instance
                    ) as mock_aggregator:
                        # Capture stdout
                        with mock.patch("sys.stdout", new=StringIO()) as fake_stdout:
                            # Call the main function
                            main()

                            # Check that the configuration was loaded
                            assert (
                                f"Configuration loaded from '{config_path}'"
                                in fake_stdout.getvalue()
                            )

                            # Check that CodeAggregator was called with the merged args
                            mock_aggregator.assert_called_once()
                            call_args = mock_aggregator.call_args[1]
                            assert call_args["directory"] == test_config["directory"]
                            assert (
                                call_args["output_file"] == test_config["output_file"]
                            )
                            assert call_args["include_files"] == {
                                test_config["include_files"]
                            }
                            assert (
                                call_args["summary_mode"] == test_config["summary_mode"]
                            )
                            assert (
                                call_args["include_comments"]
                                == test_config["include_comments"]
                            )


def test_load_nonexistent_config_in_main():
    """Checks that we handle missing config files without crashing."""
    nonexistent_path = "/path/to/nonexistent/config.json"

    # Create args with load_config pointing to non-existent file
    args = argparse.Namespace(
        load_config=nonexistent_path,
        # Other args not relevant for this test
    )

    # Mock parse_arguments
    with mock.patch("promptprep.cli.parse_arguments", return_value=args):
        # Mock load_config to raise FileNotFoundError
        error_msg = f"Configuration file '{nonexistent_path}' not found."
        with mock.patch(
            "promptprep.config.ConfigManager.load_config",
            side_effect=FileNotFoundError(error_msg),
        ):
            # Redirect stderr and catch SystemExit
            with mock.patch("sys.stderr", new=StringIO()) as fake_stderr:
                with pytest.raises(SystemExit) as exc_info:
                    main()

                # Check exit code
                assert exc_info.value.code == 1

                # Check error message
                assert f"Error: {error_msg}" in fake_stderr.getvalue()
