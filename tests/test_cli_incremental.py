import os
import tempfile
import time
from unittest import mock
from io import StringIO
import sys

from promptprep.cli import parse_arguments, main


def test_incremental_args_parsing():
    """Checks if we properly handle incremental processing arguments."""
    # Test with incremental flag
    with mock.patch.object(sys, "argv", ["promptprep", "--incremental"]):
        args = parse_arguments()
        assert args.incremental is True
        assert args.last_run_timestamp is None

    # Test with timestamp
    timestamp = "1620000000"
    with mock.patch.object(
        sys, "argv", ["promptprep", "--incremental", "--last-run-timestamp", timestamp]
    ):
        args = parse_arguments()
        assert args.incremental is True
        assert args.last_run_timestamp == float(timestamp)


def test_main_with_incremental():
    """Verifies that incremental processing works as expected."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test file
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write('print("Hello World")')

        # Mock args with incremental mode
        args_mock = mock.Mock()
        args_mock.incremental = True
        args_mock.last_run_timestamp = time.time() - 1000  # 1000 seconds ago
        args_mock.directory = tmpdir
        args_mock.output_file = "output.txt"
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
        args_mock.save_config = None
        args_mock.template_file = None
        args_mock.prev_file = None
        args_mock.diff_output = None
        args_mock.diff_context = 3

        # Mock the CodeAggregator constructor
        mock_constructor = mock.Mock(return_value=mock.Mock())

        with (
            mock.patch("promptprep.cli.parse_arguments", return_value=args_mock),
            mock.patch("promptprep.cli.CodeAggregator", mock_constructor),
            mock.patch("sys.stdout", new=StringIO()) as fake_stdout,
        ):
            main()

            # Verify CodeAggregator was created with incremental=True
            _, kwargs = mock_constructor.call_args
            assert kwargs["incremental"] is True
            assert kwargs["last_run_timestamp"] == args_mock.last_run_timestamp

            # Verify some output was generated
            assert "created successfully" in fake_stdout.getvalue()


def test_main_with_incremental_no_timestamp():
    """Makes sure we handle incremental mode without a timestamp properly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock args with incremental mode but no timestamp
        args_mock = mock.Mock()
        args_mock.incremental = True
        args_mock.last_run_timestamp = None
        args_mock.directory = tmpdir
        args_mock.output_file = "output.txt"
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
        args_mock.save_config = None
        args_mock.template_file = None
        args_mock.prev_file = None
        args_mock.diff_output = None
        args_mock.diff_context = 3

        # Mock the CodeAggregator constructor
        mock_constructor = mock.Mock(return_value=mock.Mock())

        with (
            mock.patch("promptprep.cli.parse_arguments", return_value=args_mock),
            mock.patch("promptprep.cli.CodeAggregator", mock_constructor),
            mock.patch("sys.stdout", new=StringIO()) as fake_stdout,
        ):
            main()

            # Verify CodeAggregator was created with incremental=True but timestamp=None
            _, kwargs = mock_constructor.call_args
            assert kwargs["incremental"] is True
            assert kwargs["last_run_timestamp"] is None

            # Verify some output was generated
            assert "created successfully" in fake_stdout.getvalue()


def test_incremental_with_clipboard():
    """Checks that incremental mode works with clipboard output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock args with incremental mode and clipboard
        args_mock = mock.Mock()
        args_mock.incremental = True
        args_mock.last_run_timestamp = time.time() - 1000
        args_mock.directory = tmpdir
        args_mock.output_file = "output.txt"
        args_mock.clipboard = True
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
        args_mock.save_config = None
        args_mock.template_file = None
        args_mock.prev_file = None
        args_mock.diff_output = None
        args_mock.diff_context = 3

        # Mock aggregator with successful clipboard copy
        mock_aggregator = mock.Mock()
        mock_aggregator.aggregate_code.return_value = "Incremental content"
        mock_aggregator.copy_to_clipboard.return_value = True

        with (
            mock.patch("promptprep.cli.parse_arguments", return_value=args_mock),
            mock.patch("promptprep.cli.CodeAggregator", return_value=mock_aggregator),
            mock.patch("sys.stdout", new=StringIO()) as fake_stdout,
        ):
            main()

            # Verify copy_to_clipboard was called
            mock_aggregator.copy_to_clipboard.assert_called_once()

            # Verify the output message
            assert "copied to the clipboard successfully" in fake_stdout.getvalue()


def test_unix_timestamp_parsing():
    """Ensures we can parse Unix timestamps correctly."""
    # Test Unix timestamp as float
    unix_time = "1681574645.0"
    with mock.patch.object(
        sys, "argv", ["promptprep", "--incremental", "--last-run-timestamp", unix_time]
    ):
        args = parse_arguments()
        assert args.incremental is True
        assert args.last_run_timestamp == float(unix_time)
