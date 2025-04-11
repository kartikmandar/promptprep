import os
import subprocess
import sys
import tempfile
import pytest
from unittest import mock
import platform

# Fix the path to the CLI script (PromptPrep instead of promptprep)
SCRIPT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "PromptPrep", "cli.py")

# Add import for CodeAggregator class for direct testing
from PromptPrep.aggregator import CodeAggregator, DirectoryTreeGenerator


def run_script(args, cwd):
    cmd = [sys.executable, SCRIPT_PATH] + args
    print(f"Running command: {' '.join(cmd)}")
    print(f"Working directory: {cwd}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    print(f"Exit code: {result.returncode}")
    print(f"Standard output: {result.stdout}")
    print(f"Error output: {result.stderr}")
    return result


def test_default_output():
    with tempfile.TemporaryDirectory() as tmpdir:
        run_script(["-d", tmpdir], cwd=tmpdir)
        output_file = os.path.join(tmpdir, "full_code.txt")
        assert os.path.exists(output_file)
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert "Directory Tree:" in content


def test_specified_directory():
    with tempfile.TemporaryDirectory() as src_dir:
        dummy_file = os.path.join(src_dir, "dummy.py")
        with open(dummy_file, "w", encoding="utf-8") as f:
            f.write("print('hello from dummy')")
        with tempfile.TemporaryDirectory() as work_dir:
            custom_output = "test_output.txt"
            run_script(["-d", src_dir, "-o", custom_output], cwd=work_dir)
            output_file = os.path.join(work_dir, custom_output)
            assert os.path.exists(output_file)
            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()
            assert "dummy.py" in content


def test_include_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = os.path.join(tmpdir, "dummy.py")
        with open(file1, "w", encoding="utf-8") as f:
            f.write("print('dummy')")
        file2 = os.path.join(tmpdir, "extra.py")
        with open(file2, "w", encoding="utf-8") as f:
            f.write("print('extra')")
        run_script(["-d", tmpdir, "-i", "dummy.py"], cwd=tmpdir)
        output_file = os.path.join(tmpdir, "full_code.txt")
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert "dummy.py" in content
        assert "extra.py" not in content


def test_extensions():
    with tempfile.TemporaryDirectory() as tmpdir:
        py_file = os.path.join(tmpdir, "dummy.py")
        with open(py_file, "w", encoding="utf-8") as f:
            f.write("print('Python')")
        txt_file = os.path.join(tmpdir, "dummy.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("Text file content")
        run_script(["-d", tmpdir, "-x", ".py"], cwd=tmpdir)
        output_file = os.path.join(tmpdir, "full_code.txt")
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert "dummy.py" in content
        assert "Text file content" not in content


def test_exclude_dirs():
    with tempfile.TemporaryDirectory() as tmpdir:
        exclude_dir = os.path.join(tmpdir, "exclude_this")
        os.mkdir(exclude_dir)
        file_in_exclude = os.path.join(exclude_dir, "dummy.py")
        with open(file_in_exclude, "w", encoding="utf-8") as f:
            f.write("print('excluded')")
        run_script(["-d", tmpdir, "-e", "exclude_this"], cwd=tmpdir)
        output_file = os.path.join(tmpdir, "full_code.txt")
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert "exclude_this/ [EXCLUDED]" in content
        assert "dummy.py" not in content


def test_copy_to_clipboard():
    """Test clipboard functionality with mocked subprocess."""
    with tempfile.TemporaryDirectory() as tmpdir:
        dummy_file = os.path.join(tmpdir, "dummy.py")
        with open(dummy_file, "w", encoding="utf-8") as f:
            f.write("print('hello world')")
        
        aggregator = CodeAggregator(directory=tmpdir)
        content = aggregator.aggregate_code()
        
        # Test with mocked subprocess for each platform
        with mock.patch('platform.system', return_value='Darwin'), \
             mock.patch('subprocess.Popen') as mock_popen:
            mock_process = mock.Mock()
            mock_popen.return_value = mock_process
            mock_process.communicate.return_value = (None, None)
            
            result = aggregator.copy_to_clipboard(content)
            assert result is True
            mock_popen.assert_called_once_with("pbcopy", env={"LANG": "en_US.UTF-8"}, stdin=subprocess.PIPE)
        
        with mock.patch('platform.system', return_value='Windows'), \
             mock.patch('subprocess.Popen') as mock_popen:
            mock_process = mock.Mock()
            mock_popen.return_value = mock_process
            mock_process.communicate.return_value = (None, None)
            
            result = aggregator.copy_to_clipboard(content)
            assert result is True
            mock_popen.assert_called_once_with("clip", stdin=subprocess.PIPE)
        
        with mock.patch('platform.system', return_value='Linux'), \
             mock.patch('subprocess.Popen') as mock_popen, \
             mock.patch('builtins.print') as mock_print:
            # First successful case - xclip is available
            mock_process = mock.Mock()
            mock_popen.return_value = mock_process
            mock_process.communicate.return_value = (None, None)
            
            result = aggregator.copy_to_clipboard(content)
            assert result is True
            mock_popen.assert_called_once_with(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            
            # Reset mocks
            mock_popen.reset_mock()
            
            # Second case - xclip fails, xsel works
            mock_popen.side_effect = [FileNotFoundError, mock_process]
            
            result = aggregator.copy_to_clipboard(content)
            assert result is True
            assert mock_popen.call_count == 2
            
            # Reset mocks
            mock_popen.reset_mock()
            
            # Third case - both fail
            mock_popen.side_effect = FileNotFoundError
            
            result = aggregator.copy_to_clipboard(content)
            assert result is False
            mock_print.assert_called_with("Could not find clipboard command. Please install xclip or xsel.")
            
        with mock.patch('platform.system', return_value='Unknown'), \
             mock.patch('builtins.print') as mock_print:
            result = aggregator.copy_to_clipboard(content)
            assert result is False
            mock_print.assert_called_with("Clipboard operations not supported on Unknown")


def test_tree_generator():
    """Test the DirectoryTreeGenerator directly"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create sample directory structure
        os.mkdir(os.path.join(tmpdir, "subdir"))
        os.mkdir(os.path.join(tmpdir, "excluded_dir"))
        with open(os.path.join(tmpdir, "file1.txt"), "w") as f:
            f.write("test content")
        with open(os.path.join(tmpdir, "subdir", "file2.py"), "w") as f:
            f.write("print('hello')")
        
        # Test with default exclude_dirs
        generator = DirectoryTreeGenerator()
        tree = generator.generate(tmpdir)
        assert os.path.basename(tmpdir) + "/" in tree
        assert "subdir/" in tree
        assert "file1.txt" in tree
        assert "file2.py" in tree
        
        # Test with explicit exclude_dirs
        generator = DirectoryTreeGenerator(exclude_dirs={"subdir"})
        tree = generator.generate(tmpdir)
        assert os.path.basename(tmpdir) + "/" in tree
        assert "subdir/ [EXCLUDED]" in tree
        assert "file1.txt" in tree
        assert "file2.py" not in tree
        
        # Test with include_files
        generator = DirectoryTreeGenerator(include_files={"file1.txt"})
        tree = generator.generate(tmpdir)
        assert os.path.basename(tmpdir) + "/" in tree
        assert "subdir/" in tree
        assert "file1.txt" in tree
        assert "file2.py" not in tree


def test_tree_generator_with_extensions():
    """Test the DirectoryTreeGenerator with programming extensions filter"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create sample files with different extensions
        with open(os.path.join(tmpdir, "code.py"), "w") as f:
            f.write("print('hello')")
        with open(os.path.join(tmpdir, "readme.md"), "w") as f:
            f.write("# README")
        with open(os.path.join(tmpdir, "data.txt"), "w") as f:
            f.write("plain text")
            
        # Test with programming extensions filter
        generator = DirectoryTreeGenerator(programming_extensions={".py", ".md"})
        tree = generator.generate(tmpdir)
        
        # Only .py and .md files should be included
        assert "code.py" in tree
        assert "readme.md" in tree
        assert "data.txt" not in tree
        
        # Test with multiple filters combined
        generator = DirectoryTreeGenerator(
            programming_extensions={".py"}, 
            exclude_files={"readme.md"}
        )
        tree = generator.generate(tmpdir)
        
        # Only .py files should be included, readme.md should be excluded
        assert "code.py" in tree
        assert "readme.md" not in tree
        assert "data.txt" not in tree


def test_error_handling():
    """Test error handling in file reading"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test file
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write("print('test')")
        
        aggregator = CodeAggregator(directory=tmpdir)
        
        # Test file read error
        with mock.patch('builtins.open', side_effect=UnicodeDecodeError('utf-8', b'test', 0, 1, 'test error')):
            content = aggregator.aggregate_code()
            assert "Error reading file" in content


def test_clipboard_failures():
    """Test clipboard failures on different platforms"""
    with tempfile.TemporaryDirectory() as tmpdir:
        aggregator = CodeAggregator(directory=tmpdir)
        test_content = "Test content"
        
        # Test macOS failure
        with mock.patch('platform.system', return_value='Darwin'), \
             mock.patch('subprocess.Popen', side_effect=Exception("Test error")), \
             mock.patch('builtins.print') as mock_print:
            result = aggregator.copy_to_clipboard(test_content)
            assert result is False
            mock_print.assert_called_with("Error copying to clipboard: Test error")
        
        # Test Windows failure
        with mock.patch('platform.system', return_value='Windows'), \
             mock.patch('subprocess.Popen', side_effect=Exception("Test error")), \
             mock.patch('builtins.print') as mock_print:
            result = aggregator.copy_to_clipboard(test_content)
            assert result is False
            mock_print.assert_called_with("Error copying to clipboard: Test error")


def test_edge_cases():
    """Test edge cases in the aggregator"""
    # Test with empty directory
    with tempfile.TemporaryDirectory() as tmpdir:
        aggregator = CodeAggregator(directory=tmpdir)
        content = aggregator.aggregate_code()
        assert "Directory Tree:" in content
        assert os.path.basename(tmpdir) in content
    
    # Test with custom exclude files
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "exclude_me.py")
        with open(test_file, "w") as f:
            f.write("print('exclude me')")
        
        aggregator = CodeAggregator(
            directory=tmpdir,
            exclude_files={"exclude_me.py"}
        )
        content = aggregator.aggregate_code()
        assert "exclude_me.py" not in content


def test_should_exclude():
    """Test the should_exclude method directly"""
    aggregator = CodeAggregator(
        exclude_dirs={"excluded_dir"},
        exclude_files={"excluded_file.py"}
    )
    
    # Test path with excluded directory
    assert aggregator.should_exclude("excluded_dir/file.py") is True
    assert aggregator.should_exclude("parent/excluded_dir/file.py") is True
    
    # Test path with excluded file
    assert aggregator.should_exclude("excluded_file.py") is True
    assert aggregator.should_exclude("dir/excluded_file.py") is True
    
    # Test paths that shouldn't be excluded
    assert aggregator.should_exclude("allowed.py") is False
    assert aggregator.should_exclude("allowed_dir/file.py") is False


def test_is_programming_file():
    """Test the is_programming_file method"""
    aggregator = CodeAggregator()
    
    # Test standard programming files
    assert aggregator.is_programming_file("test.py") is True
    assert aggregator.is_programming_file("test.js") is True
    assert aggregator.is_programming_file("test.java") is True
    
    # Test case insensitivity
    assert aggregator.is_programming_file("test.PY") is True
    assert aggregator.is_programming_file("test.Py") is True
    
    # Test non-programming files
    assert aggregator.is_programming_file("test.txt") is False
    assert aggregator.is_programming_file("test.log") is False
    assert aggregator.is_programming_file("test") is False
    
    # Test with custom extensions
    custom_aggregator = CodeAggregator(programming_extensions={".custom"})
    assert custom_aggregator.is_programming_file("test.custom") is True
    assert custom_aggregator.is_programming_file("test.py") is False


def test_non_existent_directory():
    """Test handling of non-existent directories, ensuring the Directory not found check works."""
    non_existent_dir = "/this/path/definitely/does/not/exist"
    
    # Create aggregator with non-existent directory
    aggregator = CodeAggregator(directory=non_existent_dir)
    
    # Mock generate method to ensure it returns a string with "Directory not found"
    with mock.patch.object(
        aggregator.tree_generator, 
        'generate',
        side_effect=lambda x: f"Directory not found: {x}\n"
    ):
        # Call aggregate_code
        content = aggregator.aggregate_code()
        
        # Verify early return happens due to "Directory not found" check
        assert "Directory Tree:" in content
        assert "Directory not found:" in content
        assert content.strip().endswith("Directory not found: " + non_existent_dir)
        
        # Ensure no additional content is processed
        assert "# ======================" not in content


def test_linux_clipboard_partial_failure():
    """Test Linux clipboard with partial command availability"""
    with tempfile.TemporaryDirectory() as tmpdir:
        aggregator = CodeAggregator(directory=tmpdir)
        test_content = "Test content"
        
        # Test Linux with xclip failing but xsel working
        with mock.patch('platform.system', return_value='Linux'), \
             mock.patch('subprocess.Popen') as mock_popen:
            mock_process = mock.Mock()
            mock_popen.side_effect = [FileNotFoundError, mock_process]
            mock_process.communicate.return_value = (None, None)
            
            result = aggregator.copy_to_clipboard(test_content)
            assert result is True
            assert mock_popen.call_count == 2


def test_write_to_file_with_explicit_params():
    """Test write_to_file with explicitly provided parameters"""
    with tempfile.TemporaryDirectory() as tmpdir:
        aggregator = CodeAggregator(directory=tmpdir)
        test_content = "Test explicit content"
        custom_filename = os.path.join(tmpdir, "custom_output.txt")
        
        # Test with explicit content and filename
        aggregator.write_to_file(content=test_content, filename=custom_filename)
        
        # Verify file was created with correct content
        assert os.path.exists(custom_filename)
        with open(custom_filename, 'r') as f:
            content = f.read()
            assert content == test_content


def test_aggregate_code_with_nonexistent_directory_actual():
    # Use a directory path that almost certainly does not exist.
    fake_dir = "/this/path/definitely/does/not/exist"
    aggregator = CodeAggregator(directory=fake_dir)
    output = aggregator.aggregate_code()
    assert "Directory Tree:" in output
    assert f"Directory not found: {fake_dir}" in output
    # Ensure no file content is appended (i.e. no "# ======================"
    # Ensure that the directory tree generator returns the correct error message
    tree_generator = DirectoryTreeGenerator()
    tree = tree_generator.generate(fake_dir)
    assert f"Directory not found: {fake_dir}\n" == tree
    # Ensure that the aggregator returns the correct error message
    assert output == f"Directory Tree:\n{tree}\n\n"

