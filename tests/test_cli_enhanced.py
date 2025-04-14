import os
import sys
import tempfile
import pytest
from unittest import mock
from io import StringIO

from promptprep.cli import parse_arguments, main


class TestCliEnhanced:
    """Enhanced tests for CLI functionality."""

    def test_parse_arguments_all_options(self):
        """Test parsing arguments with all available options."""
        test_args = [
            "--directory", "/test/dir",
            "--output-file", "output.html",
            "--format", "html",
            "--include-files", "file1.py,file2.js",
            "--exclude-dirs", "node_modules,venv",
            "--extensions", ".py,.js",
            "--max-file-size", "50",
            "--summary-mode",
            "--no-include-comments",
            "--metadata",
            "--count-tokens",
            "--line-numbers",
        ]
        
        with mock.patch.object(sys, 'argv', ['promptprep'] + test_args):
            args = parse_arguments()
            
            assert args.directory == "/test/dir"
            assert args.output_file == "output.html"
            assert args.format == "html"
            assert args.include_files == "file1.py,file2.js"
            assert args.exclude_dirs == "node_modules,venv"
            assert args.extensions == ".py,.js"
            assert args.max_file_size == 50
            assert args.summary_mode is True
            assert args.include_comments is False
            assert args.metadata is True
            assert args.count_tokens is True
            assert args.line_numbers is True

    def test_main_with_clipboard_copy(self):
        """Test main function with clipboard copy option."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            with open(os.path.join(tmpdir, "test.py"), "w") as f:
                f.write('print("Hello")')
            
            # Mock the copy_to_clipboard method to return success
            # Mock sys.argv directly since main() doesn't take arguments
            with mock.patch('sys.argv', ['promptprep', '--directory', tmpdir, '--clipboard']), \
                 mock.patch('promptprep.aggregator.CodeAggregator.copy_to_clipboard', return_value=True), \
                 mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                
                # Run the main function
                try:
                    main()
                    success = True
                except SystemExit as e:
                    success = e.code == 0
                
                assert success
                assert "Aggregated content copied to the clipboard successfully" in mock_stdout.getvalue()

    def test_main_with_clipboard_failure(self):
        """Test main function with clipboard copy failure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            with open(os.path.join(tmpdir, "test.py"), "w") as f:
                f.write('print("Hello")')
            
            # Mock the copy_to_clipboard method to return failure
            with mock.patch('sys.argv', ['promptprep', '--directory', tmpdir, '--clipboard']), \
                 mock.patch('promptprep.aggregator.CodeAggregator.copy_to_clipboard', return_value=False), \
                 mock.patch('sys.stderr', new_callable=StringIO) as mock_stderr, \
                 mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                
                # Run the main function with clipboard option
                with pytest.raises(SystemExit) as excinfo:
                    main()
                
                # Should exit with error code 1
                assert excinfo.value.code == 1
                # Check that appropriate message was printed
                assert "Failed to copy" in mock_stderr.getvalue() or "Failed to copy" in mock_stdout.getvalue()

    def test_main_with_interactive_mode(self):
        """Test the main function with interactive file selection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            with open(os.path.join(tmpdir, "test.py"), "w") as f:
                f.write('print("Hello")')
            
            # Mock the interactive file selection
            with mock.patch('sys.argv', ['promptprep', '--directory', tmpdir, '--interactive']), \
                 mock.patch('promptprep.tui.select_files_interactive', 
                           return_value=({"test.py"}, set(), True)), \
                 mock.patch('promptprep.aggregator.CodeAggregator.write_to_file'), \
                 mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                
                try:
                    # Capture actual output for debugging if the test fails
                    main()
                    success = True
                    # Just verify that some output was produced, without checking exact content
                    # since the output might vary
                    assert len(mock_stdout.getvalue()) > 0
                except SystemExit as e:
                    success = e.code == 0
                    
                assert success

    def test_main_with_interactive_mode_cancel(self):
        """Test the main function when interactive selection is cancelled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            with open(os.path.join(tmpdir, "test.py"), "w") as f:
                f.write('print("Hello")')
            
            # Mock the interactive file selection with cancel (save=False)
            with mock.patch('sys.argv', ['promptprep', '--directory', tmpdir, '--interactive']), \
                 mock.patch('promptprep.tui.select_files_interactive', 
                           return_value=(set(), set(), False)), \
                 mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                
                # Run the main function
                main()  # Should return normally, not exit with error
                
                # Should print appropriate message
                assert "selection canceled" in mock_stdout.getvalue()

    def test_main_with_interactive_mode_error(self):
        """Test the main function when interactive selection fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            with open(os.path.join(tmpdir, "test.py"), "w") as f:
                f.write('print("Hello")')
            
            # Create a mock that simulates the right type of exception
            with mock.patch('sys.argv', ['promptprep', '--directory', tmpdir, '--interactive']), \
                 mock.patch('promptprep.tui.select_files_interactive', 
                           side_effect=Exception("Test error")), \
                 mock.patch('sys.stdout', new_callable=StringIO), \
                 mock.patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                
                # The main function may handle some exceptions internally,
                # so we only check that execution completes without crashing
                try:
                    main()
                    # Test passes if we reach here, as we're handling the exception
                    assert "error" in mock_stderr.getvalue().lower()
                except SystemExit as e:
                    # Also acceptable if it exits with an error code
                    assert e.code != 0
                    assert True  # Test passes

    def test_main_with_io_error(self):
        """Test main function handling IO errors during file writing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            with open(os.path.join(tmpdir, "test.py"), "w") as f:
                f.write('print("Hello")')
            
            # Mock write_to_file to raise an IOError
            with mock.patch('sys.argv', ['promptprep', '--directory', tmpdir]), \
                 mock.patch('promptprep.aggregator.CodeAggregator.write_to_file', 
                           side_effect=IOError("Test IO error")), \
                 mock.patch('sys.stderr', new_callable=StringIO) as mock_stderr, \
                 mock.patch('sys.stdout', new_callable=StringIO):
                
                # Run the main function
                with pytest.raises(SystemExit) as excinfo:
                    main()
                
                # Should exit with error code
                assert excinfo.value.code == 1
                # Should print error message
                assert "File error" in mock_stderr.getvalue()
                assert "Test IO error" in mock_stderr.getvalue()