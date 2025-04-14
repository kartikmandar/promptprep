import os
import tempfile
import pytest
from unittest import mock
from io import StringIO
import sys

from promptprep.cli import parse_arguments, main
from promptprep.aggregator import CodeAggregator

def test_diff_args_parsing():
    """Verifies we understand all diff-related command options."""
    prev_file = "old.txt"
    with mock.patch.object(sys, 'argv', ['promptprep', '--diff', prev_file]):
        args = parse_arguments()
        assert args.prev_file == prev_file
        assert args.diff_context == 3  # Default
    
    # With custom context
    context = "5"
    with mock.patch.object(sys, 'argv', ['promptprep', '--diff', prev_file, '--diff-context', context]):
        args = parse_arguments()
        assert args.prev_file == prev_file
        assert args.diff_context == int(context)
    
    # With output file
    output = "diff.txt"
    with mock.patch.object(sys, 'argv', ['promptprep', '--diff', prev_file, '--diff-output', output]):
        args = parse_arguments()
        assert args.prev_file == prev_file
        assert args.diff_output == output

def test_main_with_diff():
    """Makes sure our diff functionality works correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create two files with different content
        file1 = os.path.join(tmpdir, "old.txt")
        file2 = os.path.join(tmpdir, "new.txt")
        
        with open(file1, "w") as f:
            f.write("Line 1\nLine 2\nLine 3")
        
        with open(file2, "w") as f:
            f.write("Line 1\nModified\nLine 3")
        
        # Mock arguments for diff
        args_mock = mock.Mock()
        args_mock.prev_file = file1
        args_mock.output_file = file2
        args_mock.diff_output = None
        args_mock.diff_context = 3
        args_mock.directory = os.getcwd()
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
        args_mock.incremental = False
        args_mock.last_run_timestamp = None
        
        # Setup compare_files mock to return a test diff
        mock_diff = "- Line 2\n+ Modified"
        
        # Mock the aggregator and its methods
        mock_aggregator = mock.Mock()
        mock_aggregator.compare_files.return_value = mock_diff
        
        with mock.patch('promptprep.cli.parse_arguments', return_value=args_mock), \
             mock.patch('promptprep.cli.CodeAggregator', return_value=mock_aggregator), \
             mock.patch('os.path.exists', return_value=True), \
             mock.patch('sys.stdout', new=StringIO()) as fake_stdout:
            
            main()
            
            # Verify compare_files was called with correct arguments
            mock_aggregator.compare_files.assert_called_once_with(
                file1=file1,
                file2=file2, 
                output_file=None,
                context_lines=3
            )
            
            # Verify output contains diff
            assert mock_diff in fake_stdout.getvalue()

def test_main_with_diff_output_file():
    """Checks that we can save diff results to a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create input files
        file1 = os.path.join(tmpdir, "old.txt")
        file2 = os.path.join(tmpdir, "new.txt")
        diff_output = os.path.join(tmpdir, "diff.txt")
        
        with open(file1, "w") as f:
            f.write("Line 1\nLine 2\nLine 3")
        
        with open(file2, "w") as f:
            f.write("Line 1\nModified\nLine 3")
        
        # Mock arguments
        args_mock = mock.Mock()
        args_mock.prev_file = file1
        args_mock.output_file = file2
        args_mock.diff_output = diff_output
        args_mock.diff_context = 3
        args_mock.directory = os.getcwd()
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
        args_mock.incremental = False
        args_mock.last_run_timestamp = None
        
        # Mock the return value of compare_files
        mock_diff_message = f"Diff written to {diff_output}"
        
        mock_aggregator = mock.Mock()
        mock_aggregator.compare_files.return_value = mock_diff_message
        
        with mock.patch('promptprep.cli.parse_arguments', return_value=args_mock), \
             mock.patch('promptprep.cli.CodeAggregator', return_value=mock_aggregator), \
             mock.patch('os.path.exists', return_value=True), \
             mock.patch('sys.stdout', new=StringIO()) as fake_stdout:
            
            main()
            
            # Verify compare_files was called with correct arguments including output file
            mock_aggregator.compare_files.assert_called_once_with(
                file1=file1,
                file2=file2, 
                output_file=diff_output,
                context_lines=3
            )
            
            # Verify output message
            assert mock_diff_message in fake_stdout.getvalue()

def test_main_with_diff_missing_previous_file():
    """Verifies we handle missing previous files gracefully."""
    nonexistent_file = "/path/that/does/not/exist.txt"
    
    # Mock arguments
    args_mock = mock.Mock()
    args_mock.prev_file = nonexistent_file
    args_mock.output_file = "output.txt"
    args_mock.diff_context = 3
    args_mock.directory = os.getcwd()
    args_mock.clipboard = False
    
    with mock.patch('promptprep.cli.parse_arguments', return_value=args_mock), \
         mock.patch('os.path.exists', return_value=False), \
         mock.patch('sys.stderr', new=StringIO()) as fake_stderr, \
         pytest.raises(SystemExit) as excinfo:
        
        main()
        
        # Verify exit code and error message
        assert excinfo.value.code == 1
        assert f"Error: Previous file not found: {nonexistent_file}" in fake_stderr.getvalue()

def test_main_with_diff_generate_current_file():
    """Makes sure we can generate the current file if needed for diff."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create previous file
        prev_file = os.path.join(tmpdir, "old.txt")
        current_file = os.path.join(tmpdir, "new.txt")
        
        with open(prev_file, "w") as f:
            f.write("Line 1\nLine 2\nLine 3")
        
        # Mock arguments
        args_mock = mock.Mock()
        args_mock.prev_file = prev_file
        args_mock.output_file = current_file
        args_mock.diff_output = None
        args_mock.diff_context = 3
        args_mock.directory = os.getcwd()
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
        args_mock.incremental = False
        args_mock.last_run_timestamp = None
        
        # Mock the aggregator and its methods
        mock_aggregator = mock.Mock()
        mock_diff = "Sample diff output"
        mock_aggregator.compare_files.return_value = mock_diff
        
        # First return False (current file doesn't exist), then True after generation
        os_path_exists_returns = [True, False, True] 
        
        with mock.patch('promptprep.cli.parse_arguments', return_value=args_mock), \
             mock.patch('promptprep.cli.CodeAggregator', return_value=mock_aggregator), \
             mock.patch('os.path.exists', side_effect=os_path_exists_returns), \
             mock.patch('sys.stdout', new=StringIO()) as fake_stdout:
            
            main()
            
            # Verify write_to_file was called to generate the current file
            mock_aggregator.write_to_file.assert_called_once()
            
            # Verify compare_files was called
            mock_aggregator.compare_files.assert_called_once()
            
            # Verify the output message
            assert mock_diff in fake_stdout.getvalue()
            assert f"Current output file '{current_file}' does not exist. Generating it..." in fake_stdout.getvalue()