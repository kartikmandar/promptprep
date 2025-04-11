import argparse
import os
import sys
import tempfile
import pytest
from unittest import mock
from io import StringIO
import subprocess
from pathlib import Path



def run_script(args, cwd):
    cmd = [sys.executable, os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "PromptPrep", "cli.py")]
    print(f"Running command: {' '.join(cmd)}")
    print(f"Working directory: {cwd}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    print(f"Exit code: {result.returncode}")
    print(f"Standard output: {result.stdout}")
    print(f"Error output: {result.stderr}")
    return result

# Import the CLI module functions directly for testing
from PromptPrep.cli import parse_arguments, main
from PromptPrep.aggregator import CodeAggregator, DirectoryTreeGenerator


def test_parse_arguments():
    """Test basic argument parsing."""
    # Test with no args (default values)
    with mock.patch.object(sys, 'argv', ['promptprep']):
        args = parse_arguments()
        assert args.directory == os.getcwd()
        assert args.output_file == "full_code.txt"
        assert args.clipboard is False

    # Test with directory and output file
    test_dir = "/test/dir"
    test_output = "output.txt"
    with mock.patch.object(sys, 'argv', ['promptprep', '-d', test_dir, '-o', test_output]):
        args = parse_arguments()
        assert args.directory == test_dir
        assert args.output_file == test_output


def test_main_file_output():
    """Test main function with file output."""
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

        # Mock parse_arguments to return our args
        with mock.patch('PromptPrep.cli.parse_arguments', return_value=args_mock):
            # Capture stdout
            with mock.patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                assert f"Aggregated file '{args_mock.output_file}' created successfully." in fake_out.getvalue()

                # Check if file was created
                output_path = os.path.join(os.getcwd(), args_mock.output_file)
                assert os.path.exists(output_path)
                os.remove(output_path)  # Clean up


def test_main_with_invalid_directory():
    """Test main function with an invalid directory."""
    invalid_dir = "/invalid/path/that/does/not/exist"
    args_mock = mock.Mock()
    args_mock.directory = invalid_dir
    args_mock.output_file = "test_output.txt"
    args_mock.clipboard = False
    args_mock.include_files = ""
    args_mock.extensions = ""
    args_mock.exclude_dirs = ""
    args_mock.max_file_size = 100.0

    with mock.patch('PromptPrep.cli.parse_arguments', return_value=args_mock), \
         mock.patch('sys.stderr', new=StringIO()) as fake_err, \
         pytest.raises(SystemExit) as excinfo:
        main()
        assert "Error: Directory not found" in fake_err.getvalue()
        assert excinfo.value.code == 1

