import os
import sys
import curses
import pytest
from unittest import mock
from io import StringIO

from promptprep.tui import FileSelector, select_files_interactive

# Mock for curses.window object
class MockWindow:
    def __init__(self, height=24, width=80):
        self.height = height
        self.width = width
        self.content = {}
    
    def getmaxyx(self):
        return self.height, self.width
    
    def addstr(self, y, x, string, attr=0):
        self.content[(y, x)] = (string, attr)
    
    def clear(self):
        self.content = {}
    
    def refresh(self):
        pass
    
    def getch(self):
        # This would be overridden in tests
        return ord('q')  # Default to 'q' for quit

# Create proper mocks for all curses functionality
@pytest.fixture
def mock_curses(monkeypatch):
    # Mock init_pair and color_pair
    curses_mock = mock.MagicMock()
    curses_mock.COLOR_GREEN = 2
    curses_mock.COLOR_RED = 1
    curses_mock.A_BOLD = 1
    curses_mock.A_REVERSE = 4
    curses_mock.A_UNDERLINE = 2
    curses_mock.A_NORMAL = 0
    curses_mock.KEY_UP = 259
    curses_mock.KEY_DOWN = 258
    curses_mock.color_pair.side_effect = lambda x: x + 10  # Just add 10 to the number
    
    # Mock wrapper to directly call the function
    def mock_wrapper(func, *args, **kwargs):
        stdscr = MockWindow()
        return func(stdscr, *args, **kwargs)
    
    curses_mock.wrapper.side_effect = mock_wrapper
    monkeypatch.setattr("promptprep.tui.curses", curses_mock)
    return curses_mock

@pytest.fixture
def temp_dir_with_files(tmpdir):
    """Create a temporary directory with some files for testing."""
    # Create some test files and directories
    test_dir = tmpdir.mkdir("test_dir")
    file1 = test_dir.join("file1.py")
    file1.write("print('hello')")
    file2 = test_dir.join("file2.txt")
    file2.write("text content")
    
    # Create a subdirectory
    subdir = test_dir.mkdir("subdir")
    file3 = subdir.join("file3.py")
    file3.write("print('in subdir')")
    
    # Hidden files
    hidden_file = test_dir.join(".hidden.py")
    hidden_file.write("# hidden file")
    hidden_dir = test_dir.mkdir(".hidden_dir")
    
    return test_dir

class TestFileSelector:
    """Tests for the FileSelector class."""
    
    def test_init(self, temp_dir_with_files):
        """Test initialization with a valid path."""
        fs = FileSelector(str(temp_dir_with_files))
        assert fs.start_path == os.path.abspath(str(temp_dir_with_files))
        assert fs.current_path == os.path.abspath(str(temp_dir_with_files))
        assert fs.cursor_pos == 0
        assert fs.offset == 0
        assert fs.selected_items == {}
        assert fs.exclude_dirs == set()
        assert not fs.show_hidden
    
    def test_get_directory_contents(self, temp_dir_with_files):
        """Test retrieving directory contents."""
        fs = FileSelector(str(temp_dir_with_files))
        contents = fs._get_directory_contents()
        
        # Should include ".." for parent directory and all non-hidden files/dirs
        assert ".." in contents
        assert "file1.py" in contents
        assert "file2.txt" in contents
        assert "subdir" in contents
        # Hidden files should not be included by default
        assert ".hidden.py" not in contents
        assert ".hidden_dir" not in contents
    
    def test_get_directory_contents_with_hidden(self, temp_dir_with_files):
        """Test retrieving directory contents including hidden files."""
        fs = FileSelector(str(temp_dir_with_files))
        fs.show_hidden = True
        contents = fs._get_directory_contents()
        
        # Should now include hidden files
        assert ".hidden.py" in contents
        assert ".hidden_dir" in contents
    
    def test_get_directory_contents_permission_error(self, temp_dir_with_files):
        """Test handling of permission errors."""
        fs = FileSelector(str(temp_dir_with_files))
        
        # Store original path to verify change later
        original_path = fs.current_path
        parent_path = os.path.dirname(original_path)
        
        # Create a patched version that raises PermissionError on first call
        call_count = [0]  # Use a list to avoid UnboundLocalError
        
        def mock_get_contents(*args):
            call_count[0] += 1
            if call_count[0] == 1:
                # First call - raise permission error
                raise PermissionError("Test error")
            else:
                # Second call after directory change - return mock files
                # The actual function will add '..' for parent directory navigation
                return ["mock_file"]
        
        # Mock os.listdir to simulate permission error and os.path.dirname for navigation
        with mock.patch('os.listdir', side_effect=mock_get_contents), \
             mock.patch('os.path.dirname', return_value=parent_path):
            
            # Call should handle the permission error and update directory
            contents = fs._get_directory_contents()
            
            # Verify results
            assert fs.status_message.startswith("Cannot access directory")
            assert fs.current_path == parent_path
            assert "mock_file" in contents  # Just check that our mock file is in the list
            # Note: The actual implementation adds ".." for parent directory navigation
    
    def test_toggle_selection_file(self, temp_dir_with_files):
        """Test toggling selection state for a file."""
        fs = FileSelector(str(temp_dir_with_files))
        file_path = os.path.join(str(temp_dir_with_files), "file1.py")
        
        # Initial state: not selected
        assert file_path not in fs.selected_items
        
        # Toggle once: should be included
        fs._toggle_selection(file_path)
        assert file_path in fs.selected_items
        assert fs.selected_items[file_path] == True
        
        # Toggle again: should be excluded
        fs._toggle_selection(file_path)
        assert file_path in fs.selected_items
        assert fs.selected_items[file_path] == False
        
        # Toggle third time: should be removed from selections
        fs._toggle_selection(file_path)
        assert file_path not in fs.selected_items
    
    def test_toggle_selection_directory(self, temp_dir_with_files):
        """Test toggling selection state for a directory."""
        fs = FileSelector(str(temp_dir_with_files))
        dir_path = os.path.join(str(temp_dir_with_files), "subdir")
        
        # Initial state: not selected
        assert dir_path not in fs.selected_items
        assert dir_path not in fs.exclude_dirs
        
        # Toggle once: should be included
        fs._toggle_selection(dir_path)
        assert dir_path in fs.selected_items
        assert fs.selected_items[dir_path] == True
        assert dir_path not in fs.exclude_dirs
        
        # Toggle again: should be excluded
        fs._toggle_selection(dir_path)
        assert dir_path in fs.selected_items
        assert fs.selected_items[dir_path] == False
        assert dir_path in fs.exclude_dirs
        
        # Toggle third time: should be removed from selections and exclude_dirs
        fs._toggle_selection(dir_path)
        assert dir_path not in fs.selected_items
        assert dir_path not in fs.exclude_dirs
    
    def test_toggle_all_in_directory(self, temp_dir_with_files):
        """Test toggling selection for all files in current directory."""
        fs = FileSelector(str(temp_dir_with_files))
        # Setup files list manually
        fs.files = ["file1.py", "file2.txt", "subdir"]
        fs.current_path = str(temp_dir_with_files)
        
        # Initial state: none selected
        assert len(fs.selected_items) == 0
        
        # Toggle all: should select all files (not directories)
        fs._toggle_all_in_directory()
        assert len(fs.selected_items) == 2  # Only the 2 files
        assert os.path.join(str(temp_dir_with_files), "file1.py") in fs.selected_items
        assert os.path.join(str(temp_dir_with_files), "file2.txt") in fs.selected_items
        
        # Toggle all again: should deselect all
        fs._toggle_all_in_directory()
        assert len(fs.selected_items) == 0
    
    def test_get_selections(self, temp_dir_with_files):
        """Test getting selected files and excluded directories."""
        fs = FileSelector(str(temp_dir_with_files))
        # Add some selections
        file1_path = os.path.join(str(temp_dir_with_files), "file1.py")
        file2_path = os.path.join(str(temp_dir_with_files), "file2.txt")
        dir_path = os.path.join(str(temp_dir_with_files), "subdir")
        
        fs.selected_items[file1_path] = True  # Include
        fs.selected_items[file2_path] = False  # Exclude
        fs.exclude_dirs.add(dir_path)  # Exclude directory
        
        # Get selections
        include_files, exclude_dirs, save = fs.get_selections()
        
        # Check results
        assert "file1.py" in include_files  # Should be relative path
        assert dir_path in exclude_dirs  # Should be absolute path
        assert not save  # Default is not to save
    
    @mock.patch('os.path.isdir')
    def test_handle_key_navigation(self, mock_isdir, temp_dir_with_files, mock_curses):
        """Test key handling for navigation."""
        fs = FileSelector(str(temp_dir_with_files))
        fs.files = ["file1.py", "file2.txt", "subdir"]
        
        # Mock stdscr
        stdscr = MockWindow()
        
        # Test up/down navigation
        assert fs.cursor_pos == 0
        
        # Down key
        fs._handle_key(mock_curses.KEY_DOWN, stdscr)
        assert fs.cursor_pos == 1
        
        # Down key again
        fs._handle_key(mock_curses.KEY_DOWN, stdscr)
        assert fs.cursor_pos == 2
        
        # Up key
        fs._handle_key(mock_curses.KEY_UP, stdscr)
        assert fs.cursor_pos == 1
    
    @mock.patch('os.path.isdir')
    @mock.patch('promptprep.tui.os.path.join')  # Use more specific patching path
    def test_handle_key_enter(self, mock_join, mock_isdir, temp_dir_with_files, mock_curses):
        """Test enter key for directory navigation and file selection."""
        fs = FileSelector(str(temp_dir_with_files))
        fs.files = ["subdir", "file1.py"]
        
        # Setup mocks for directory navigation
        mock_isdir.side_effect = lambda path: path.endswith("subdir")
        
        # Define a non-recursive join function that doesn't call os.path.join
        def safe_join(path, file):
            if file == "subdir":
                return path + "/subdir"
            else:
                return path + "/file1.py"
                
        mock_join.side_effect = safe_join
        
        # Mock stdscr
        stdscr = MockWindow()
        
        # Test entering a directory (subdir)
        fs.cursor_pos = 0  # subdir
        fs._handle_key(ord('\n'), stdscr)
        assert fs.current_path.endswith("subdir")
        
        # Reset for testing file selection
        fs.current_path = str(temp_dir_with_files)
        fs.cursor_pos = 1  # file1.py
        
        # Test selecting a file
        fs._handle_key(ord('\n'), stdscr)
        assert any(path.endswith("file1.py") for path in fs.selected_items)
    
    def test_handle_key_space(self, temp_dir_with_files, mock_curses):
        """Test space key for toggling selection."""
        fs = FileSelector(str(temp_dir_with_files))
        fs.files = ["file1.py"]
        fs.current_path = str(temp_dir_with_files)
        
        # Mock stdscr
        stdscr = MockWindow()
        
        # Test toggling selection with space
        fs.cursor_pos = 0  # file1.py
        fs._handle_key(ord(' '), stdscr)
        assert os.path.join(str(temp_dir_with_files), "file1.py") in fs.selected_items
        assert fs.selected_items[os.path.join(str(temp_dir_with_files), "file1.py")] == True
    
    def test_handle_key_toggles(self, temp_dir_with_files, mock_curses):
        """Test keys for toggling various options."""
        fs = FileSelector(str(temp_dir_with_files))
        
        # Mock stdscr
        stdscr = MockWindow()
        
        # Test toggling hidden files
        assert not fs.show_hidden
        fs._handle_key(ord('t'), stdscr)
        assert fs.show_hidden
        
        # Test toggling all files
        fs.files = ["file1.py", "file2.txt"]
        fs.current_path = str(temp_dir_with_files)
        fs._handle_key(ord('a'), stdscr)
        assert len(fs.selected_items) > 0  # Some files should be selected
        
        # Test quit
        result = fs._handle_key(ord('q'), stdscr)
        assert not result  # Should return False to exit
        assert not fs.save_selections
        
        # Test save and exit
        result = fs._handle_key(ord('s'), stdscr)
        assert not result  # Should return False to exit
        assert fs.save_selections
    
    def test_draw_screen(self, temp_dir_with_files, mock_curses):
        """Test drawing the screen."""
        fs = FileSelector(str(temp_dir_with_files))
        fs.files = ["file1.py", "file2.txt"]
        fs.current_path = str(temp_dir_with_files)
        
        # Select a file
        file_path = os.path.join(str(temp_dir_with_files), "file1.py")
        fs.selected_items[file_path] = True
        
        # Mock stdscr
        stdscr = MockWindow(24, 80)
        
        # Draw screen
        fs._draw_screen(stdscr)
        
        # Check that some key elements were drawn
        assert ("PromptPrep - Interactive File Selector", mock_curses.A_BOLD) in stdscr.content.values()
    
    @mock.patch('promptprep.tui.FileSelector.run')
    def test_select_files_interactive(self, mock_run, temp_dir_with_files, mock_curses):
        """Test the select_files_interactive function."""
        # Setup mock return value
        mock_run.return_value = (set(["file1.py"]), set(["/path/to/excluded"]), True)
        
        # Call the function
        include_files, exclude_dirs, save = select_files_interactive(str(temp_dir_with_files))
        
        # Check results
        assert include_files == set(["file1.py"])
        assert exclude_dirs == set(["/path/to/excluded"])
        assert save == True
    
    def test_select_files_interactive_exception(self, temp_dir_with_files):
        """Test exception handling in select_files_interactive."""
        # Mock curses.wrapper to raise an exception
        with mock.patch('curses.wrapper', side_effect=Exception("Test error")):
            # Capture stderr
            stderr_capture = StringIO()
            with mock.patch('sys.stderr', stderr_capture):
                include_files, exclude_dirs, save = select_files_interactive(str(temp_dir_with_files))
            
            # Check results
            assert "Error in interactive mode: Test error" in stderr_capture.getvalue()
            assert include_files == set()
            assert exclude_dirs == set()
            assert save == False