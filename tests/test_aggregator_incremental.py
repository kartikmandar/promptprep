import os
import tempfile
import time
import pytest
from unittest import mock
import datetime
from pathlib import Path

from promptprep.aggregator import CodeAggregator, DirectoryTreeGenerator


class TestIncrementalProcessing:
    """Tests for the incremental processing functionality."""
    
    def test_incremental_mode_basic(self):
        """Test basic incremental processing - only process files modified since timestamp."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create timestamp for "old" files
            old_time = time.time() - 10000  # 10000 seconds ago
            
            # Create an "old" file
            old_file = os.path.join(tmpdir, "old.py")
            with open(old_file, "w") as f:
                f.write('print("Old file")')
            os.utime(old_file, (old_time, old_time))
            
            # Simulate passage of time
            mid_time = time.time() - 5000  # 5000 seconds ago
            
            # Create a "new" file
            new_file = os.path.join(tmpdir, "new.py")
            with open(new_file, "w") as f:
                f.write('print("New file")')
            
            # Create aggregator with incremental mode enabled
            aggregator = CodeAggregator(
                directory=tmpdir,
                incremental=True,
                last_run_timestamp=mid_time
            )
            
            result = aggregator.aggregate_code()
            
            # Only new file's content should be processed
            assert 'print("New file")' in result
            assert 'print("Old file")' not in result
    
    def test_incremental_mode_modified_files(self):
        """Test incremental processing with modified files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create timestamp for "old" files
            old_time = time.time() - 10000  # 10000 seconds ago
            
            # Create files with old timestamp
            file1 = os.path.join(tmpdir, "file1.py")
            file2 = os.path.join(tmpdir, "file2.py")
            with open(file1, "w") as f:
                f.write('print("File 1 - old")')
            with open(file2, "w") as f:
                f.write('print("File 2 - old")')
            
            os.utime(file1, (old_time, old_time))
            os.utime(file2, (old_time, old_time))
            
            # Record the middle time
            mid_time = time.time() - 5000  # 5000 seconds ago
            
            # Update file2 to make it "newer"
            with open(file2, "w") as f:
                f.write('print("File 2 - new")')
            
            # Create aggregator with incremental mode
            aggregator = CodeAggregator(
                directory=tmpdir,
                incremental=True,
                last_run_timestamp=mid_time
            )
            
            result = aggregator.aggregate_code()
            
            # Only the modified file's content should be processed
            assert 'print("File 2 - new")' in result
            assert 'print("File 1 - old")' not in result
    
    def test_incremental_mode_disabled(self):
        """Test that all files are included when incremental mode is disabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create timestamp for "old" files
            old_time = time.time() - 10000  # 10000 seconds ago
            
            # Create an "old" file
            old_file = os.path.join(tmpdir, "old.py")
            with open(old_file, "w") as f:
                f.write('print("Old file")')
            os.utime(old_file, (old_time, old_time))
            
            # Create a "new" file
            new_file = os.path.join(tmpdir, "new.py")
            with open(new_file, "w") as f:
                f.write('print("New file")')
            
            # Create aggregator with incremental mode disabled
            aggregator = CodeAggregator(
                directory=tmpdir,
                incremental=False,
                last_run_timestamp=old_time
            )
            
            result = aggregator.aggregate_code()
            
            # Both files should be included
            assert "new.py" in result
            assert 'print("New file")' in result
            assert "old.py" in result
            assert 'print("Old file")' in result
    
    def test_incremental_mode_no_timestamp(self):
        """Test incremental mode without a timestamp (should process all files)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create an "old" file
            old_file = os.path.join(tmpdir, "old.py")
            with open(old_file, "w") as f:
                f.write('print("Old file")')
            
            # Create a "new" file
            new_file = os.path.join(tmpdir, "new.py")
            with open(new_file, "w") as f:
                f.write('print("New file")')
            
            # Create aggregator with incremental mode enabled but no timestamp
            aggregator = CodeAggregator(
                directory=tmpdir,
                incremental=True,
                last_run_timestamp=None
            )
            
            result = aggregator.aggregate_code()
            
            # Both files should be included when no timestamp is provided
            assert "new.py" in result
            assert 'print("New file")' in result
            assert "old.py" in result
            assert 'print("Old file")' in result

    def test_incremental_mode_with_directory_changes(self):
        """Test incremental processing with changes to directory structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create initial structure with files
            old_dir = os.path.join(tmpdir, "old_dir")
            os.makedirs(old_dir)
            old_file = os.path.join(old_dir, "old_file.py")
            with open(old_file, "w") as f:
                f.write('print("Old file")')
            
            # Set timestamp for old files
            old_time = time.time() - 10000
            os.utime(old_file, (old_time, old_time))
            os.utime(old_dir, (old_time, old_time))
            
            # Record middle timestamp
            mid_time = time.time() - 5000
            
            # Create new directory and file after the timestamp
            new_dir = os.path.join(tmpdir, "new_dir")
            os.makedirs(new_dir)
            new_file = os.path.join(new_dir, "new_file.py")
            with open(new_file, "w") as f:
                f.write('print("New file")')
            
            # Create aggregator with incremental mode
            aggregator = CodeAggregator(
                directory=tmpdir,
                incremental=True,
                last_run_timestamp=mid_time
            )
            
            result = aggregator.aggregate_code()
            
            # Only the new file should be processed
            assert 'print("New file")' in result
            assert 'print("Old file")' not in result
            
    def test_get_file_mod_time(self):
        """Test the _get_file_mod_time method."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            # Write some content
            tmp.write(b"test content")
            tmp_path = tmp.name
            
            # Set specific modification time
            mod_time = time.time() - 1000
            os.utime(tmp_path, (mod_time, mod_time))
            
            aggregator = CodeAggregator()
            
            # Get the modification time
            result = aggregator._get_file_mod_time(tmp_path)
            
            # Allow for slight differences due to filesystem precision
            assert abs(result - mod_time) < 1
            
            # Clean up
            os.unlink(tmp_path)
            
    def test_is_file_changed(self):
        """Test the _is_file_changed method with different scenarios."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test content")
            tmp_path = tmp.name
            
            # Set specific modification time
            old_time = time.time() - 1000
            os.utime(tmp_path, (old_time, old_time))
            
            # Test with incremental mode off
            aggregator1 = CodeAggregator(incremental=False, last_run_timestamp=old_time + 500)
            assert aggregator1._is_file_changed(tmp_path) is True
            
            # Test with incremental mode on but no timestamp
            aggregator2 = CodeAggregator(incremental=True, last_run_timestamp=None)
            assert aggregator2._is_file_changed(tmp_path) is True
            
            # Test with file older than timestamp
            aggregator3 = CodeAggregator(incremental=True, last_run_timestamp=old_time + 500)
            assert aggregator3._is_file_changed(tmp_path) is False
            
            # Test with file newer than timestamp
            aggregator4 = CodeAggregator(incremental=True, last_run_timestamp=old_time - 500)
            assert aggregator4._is_file_changed(tmp_path) is True
            
            # Clean up
            os.unlink(tmp_path)

    def test_file_mod_times_tracking(self):
        """Test that file modification times are correctly tracked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file
            test_file = os.path.join(tmpdir, "test.py")
            with open(test_file, "w") as f:
                f.write('print("Test file")')
            
            # Set a custom mod time to ensure it's not just current time
            mod_time = time.time() - 1000
            os.utime(test_file, (mod_time, mod_time))
            
            # Mock _get_file_mod_time to track if it's called
            with mock.patch.object(CodeAggregator, '_get_file_mod_time', return_value=mod_time) as mock_get_time:
                aggregator = CodeAggregator(
                    directory=tmpdir,
                    incremental=True,
                    last_run_timestamp=mod_time - 500  # Make file appear newer than timestamp
                )
                
                aggregator.aggregate_code()
                
                # Verify _get_file_mod_time was called for test.py
                mock_get_time.assert_called_with(test_file)


class TestFileDiffComparison:
    """Tests for file comparison and diff generation functionality."""
    
    def test_compare_files_basic(self):
        """Test basic file comparison."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as file1, \
             tempfile.NamedTemporaryFile(mode="w", delete=False) as file2:
            # Write different content to the files
            file1.write("Line 1\nLine 2\nLine 3\n")
            file2.write("Line 1\nModified Line\nLine 3\n")
            file1_path = file1.name
            file2_path = file2.name
        
        try:
            aggregator = CodeAggregator()
            diff_result = aggregator.compare_files(file1_path, file2_path)
            
            # Check that diff contains the expected changes
            assert "Line 2" in diff_result
            assert "Modified Line" in diff_result
            assert "+" in diff_result  # Addition marker
            assert "-" in diff_result  # Deletion marker
        finally:
            # Clean up
            os.unlink(file1_path)
            os.unlink(file2_path)
    
    def test_compare_files_identical(self):
        """Test comparison of identical files."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as file1, \
             tempfile.NamedTemporaryFile(mode="w", delete=False) as file2:
            # Write the same content to both files
            content = "Line 1\nLine 2\nLine 3\n"
            file1.write(content)
            file2.write(content)
            file1_path = file1.name
            file2_path = file2.name
        
        try:
            aggregator = CodeAggregator()
            diff_result = aggregator.compare_files(file1_path, file2_path)
            
            # When files are identical, the diff output should be empty or minimal
            # Check either for specific "no differences" message or just that it doesn't contain diff markers
            assert "+" not in diff_result or "-" not in diff_result
        finally:
            # Clean up
            os.unlink(file1_path)
            os.unlink(file2_path)
    
    def test_compare_files_with_output_file(self):
        """Test saving diff to an output file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as file1, \
             tempfile.NamedTemporaryFile(mode="w", delete=False) as file2, \
             tempfile.NamedTemporaryFile(mode="w", delete=False) as output_file:
            # Write different content to the files
            file1.write("Line 1\nLine 2\nLine 3\n")
            file2.write("Line 1\nModified Line\nLine 3\n")
            file1_path = file1.name
            file2_path = file2.name
            output_path = output_file.name
        
        try:
            aggregator = CodeAggregator()
            diff_result = aggregator.compare_files(file1_path, file2_path, output_file=output_path)
            
            # Check that the message about writing to file is returned
            assert "Diff written to" in diff_result
            
            # Check that the diff was written to the output file
            with open(output_path, "r") as f:
                content = f.read()
                assert "Line 2" in content
                assert "Modified Line" in content
        finally:
            # Clean up
            os.unlink(file1_path)
            os.unlink(file2_path)
            os.unlink(output_path)
    
    def test_compare_files_context_lines(self):
        """Test diff with different numbers of context lines."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as file1, \
             tempfile.NamedTemporaryFile(mode="w", delete=False) as file2:
            # Create larger files with multiple changes
            file1.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\n")
            file2.write("Line 1\nChanged 2\nLine 3\nLine 4\nChanged 5\nLine 6\nLine 7\n")
            file1_path = file1.name
            file2_path = file2.name
        
        try:
            aggregator = CodeAggregator()
            
            # Test with 1 context line
            diff_result_small = aggregator.compare_files(file1_path, file2_path, context_lines=1)
            
            # Test with 3 context lines
            diff_result_large = aggregator.compare_files(file1_path, file2_path, context_lines=3)
            
            # The diff with more context lines should be longer
            assert len(diff_result_large) > len(diff_result_small)
            
            # Both should contain the changed lines
            assert "Line 2" in diff_result_small
            assert "Changed 2" in diff_result_small
            assert "Line 5" in diff_result_small
            assert "Changed 5" in diff_result_small
            
            # But the larger context should contain more surrounding lines
            assert "Line 1" in diff_result_large  # Should be visible in more context
            assert "Line 7" in diff_result_large  # Should be visible in more context
        finally:
            # Clean up
            os.unlink(file1_path)
            os.unlink(file2_path)
    
    def test_compare_files_nonexistent(self):
        """Test comparison with nonexistent files."""
        nonexistent_file = "/path/that/does/not/exist/file.txt"
        existing_file = tempfile.NamedTemporaryFile(delete=False).name
        
        try:
            aggregator = CodeAggregator()
            
            # Test with first file nonexistent
            with pytest.raises(FileNotFoundError):
                aggregator.compare_files(nonexistent_file, existing_file)
                
            # Test with second file nonexistent
            with pytest.raises(FileNotFoundError):
                aggregator.compare_files(existing_file, nonexistent_file)
        finally:
            # Clean up
            os.unlink(existing_file)


class TestCustomFormatter:
    """Tests for custom formatter template functionality."""
    
    def test_custom_formatter_with_template(self):
        """Test using a custom formatter with a template file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a simple template file
            template_file = os.path.join(tmpdir, "template.txt")
            with open(template_file, "w") as f:
                f.write("TITLE: ${TITLE}\nCODE:\n${FILES}\nMETADATA: ${METADATA}")
            
            # Create a test code file
            code_file = os.path.join(tmpdir, "test.py")
            with open(code_file, "w") as f:
                f.write('print("Hello World")')
            
            # Mock the render_template method to return a controlled output
            with mock.patch('promptprep.formatters.CustomTemplateFormatter.render_template') as mock_render:
                # Make the mock return content with the placeholders replaced
                mock_render.return_value = "TITLE: Code Aggregation\nCODE:\nprint(\"Hello World\")\nMETADATA: None"
                
                # Create aggregator with custom format and template
                aggregator = CodeAggregator(
                    directory=tmpdir,
                    output_format="custom",
                    template_file=template_file
                )
                
                result = aggregator.aggregate_code()
                
                # Check that template placeholders were replaced in the mocked result
                assert "TITLE: Code Aggregation" in result
                assert "CODE:" in result
                assert 'print("Hello World")' in result
    
    def test_custom_formatter_missing_template(self):
        """Test error handling when template file is missing."""
        nonexistent_template = "/path/to/nonexistent/template.txt"
        
        # Create aggregator with custom format but missing template
        # The warning gets emitted during initialization, not during aggregate_code
        with pytest.warns(UserWarning, match="Failed to initialize formatter"):
            aggregator = CodeAggregator(
                output_format="custom",
                template_file=nonexistent_template
            )
            
            result = aggregator.aggregate_code()
            
            # Verify we still get some output, even with the template missing
            assert isinstance(result, str)
            assert len(result) > 0