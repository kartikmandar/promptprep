"""A friendly terminal interface for choosing which files to process."""
import curses
import os
import sys
from typing import List, Set, Tuple, Dict, Optional

class FileSelector:
    """Lets you browse and select files using arrow keys and spacebar."""
    
    def __init__(self, start_path: str):
        """Gets everything ready for file selection.
        
        Args:
            start_path: Where to start browsing from
        """
        self.start_path = os.path.abspath(start_path)
        self.current_path = self.start_path
        self.cursor_pos = 0
        self.offset = 0
        self.selected_items: Dict[str, bool] = {}  # Dictionary tracking selected items (True=include, False=exclude)
        self.exclude_dirs: Set[str] = set()  # Set of excluded directory paths
        self.files: List[str] = []
        self.show_hidden = False
        self.status_message = ""
        self.save_selections = False  # Flag to indicate whether selections should be saved
    
    def _get_directory_contents(self) -> List[str]:
        """Gets a sorted list of files and folders, optionally showing hidden items."""
        try:
            items = os.listdir(self.current_path)
            # Filter hidden files if show_hidden is False
            if not self.show_hidden:
                items = [item for item in items if not item.startswith('.')]
            # Add '..' for parent directory navigation (except at the root of the filesystem)
            if os.path.abspath(self.current_path) != os.path.abspath(os.path.sep):
                items.insert(0, "..")
            # Sort directories first, then files
            dirs = [item for item in items if os.path.isdir(os.path.join(self.current_path, item))]
            files = [item for item in items if not os.path.isdir(os.path.join(self.current_path, item))]
            return sorted(dirs) + sorted(files)
        except (PermissionError, FileNotFoundError):
            self.status_message = f"Cannot access directory: {self.current_path}"
            # Go back to parent directory
            self.current_path = os.path.dirname(self.current_path)
            return self._get_directory_contents()
    
    def _draw_screen(self, stdscr) -> None:
        """Shows the current directory contents and selection status on screen."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Draw title and current path
        title = "PromptPrep - Interactive File Selector"
        path_display = self.current_path
        if len(path_display) > width - 2:
            path_display = "..." + path_display[-(width-5):]
        
        stdscr.addstr(0, 0, title[:width-1], curses.A_BOLD)
        stdscr.addstr(1, 0, path_display[:width-1], curses.A_UNDERLINE)
        
        # Draw file list
        self.files = self._get_directory_contents()
        visible_items = height - 7  # Account for header and footer lines
        
        # Adjust offset if cursor moves outside visible area
        if self.cursor_pos < self.offset:
            self.offset = self.cursor_pos
        elif self.cursor_pos >= self.offset + visible_items:
            self.offset = self.cursor_pos - visible_items + 1
        
        # Ensure offset doesn't go negative
        self.offset = max(0, min(self.offset, len(self.files) - visible_items))
        
        # Ensure cursor is within range
        self.cursor_pos = max(0, min(self.cursor_pos, len(self.files) - 1))
        
        # Draw visible files
        for i, item in enumerate(self.files[self.offset:self.offset+visible_items], 0):
            y_pos = i + 3  # Start at line 3
            item_path = os.path.join(self.current_path, item)
            is_dir = os.path.isdir(item_path)
            is_selected = item_path in self.selected_items
            is_excluded = is_dir and item_path in self.exclude_dirs
            
            # Determine display attributes
            attrs = curses.A_NORMAL
            prefix = "  "
            
            # Show selection status
            if is_selected:
                if self.selected_items[item_path]:
                    prefix = "+ "  # Include
                    attrs |= curses.color_pair(1)  # Green
                else:
                    prefix = "- "  # Exclude
                    attrs |= curses.color_pair(2)  # Red
            
            if is_excluded:
                prefix = "X "  # Directory excluded
                attrs |= curses.color_pair(2)  # Red
            
            # Highlight current cursor position
            if i + self.offset == self.cursor_pos:
                attrs |= curses.A_REVERSE
            
            # Add directory indicator
            display_name = item + ("/" if is_dir else "")
            
            # Truncate if too long
            max_name_length = width - 4  # Account for prefix and potential truncation
            if len(display_name) > max_name_length:
                display_name = display_name[:max_name_length-3] + "..."
            
            # Draw the item
            stdscr.addstr(y_pos, 0, prefix + display_name, attrs)
        
        # Draw status line
        status_line = height - 3
        if self.status_message:
            stdscr.addstr(status_line, 0, self.status_message[:width-1])
        
        # Draw help footer - removed H key reference
        footer_line = height - 2
        help_text = "UP/DOWN: Navigate | ENTER: Open/Select | SPACE: Toggle Selection | A: Select All | T: Show Hidden | Q: Quit | S: Save"
        if len(help_text) > width:
            help_text = help_text[:width-3] + "..."
        stdscr.addstr(footer_line, 0, help_text)
        
        # Draw selection count
        selection_line = height - 1
        includes = sum(1 for value in self.selected_items.values() if value)
        excludes = len(self.selected_items) - includes + len(self.exclude_dirs)
        stdscr.addstr(selection_line, 0, f"Selected: {includes} includes, {excludes} excludes")
        
        stdscr.refresh()
    
    def _toggle_selection(self, path: str) -> None:
        """Cycles through include/exclude/unselected states for a file or directory."""
        is_dir = os.path.isdir(path)
        
        # For directories, toggle between include, exclude dir, and none
        if is_dir:
            if path in self.selected_items:
                if self.selected_items[path]:  # Currently included
                    # Change to excluded
                    self.selected_items[path] = False
                    self.exclude_dirs.add(path)
                else:  # Currently excluded
                    # Remove selection
                    del self.selected_items[path]
                    self.exclude_dirs.discard(path)
            else:
                # Not selected, add as included
                self.selected_items[path] = True
                self.exclude_dirs.discard(path)
        # For files, toggle between include, exclude, and none
        else:
            if path in self.selected_items:
                if self.selected_items[path]:  # Currently included
                    # Change to excluded
                    self.selected_items[path] = False
                else:  # Currently excluded
                    # Remove selection
                    del self.selected_items[path]
            else:
                # Not selected, add as included
                self.selected_items[path] = True
    
    def _toggle_all_in_directory(self) -> None:
        """Selects or deselects all files in the current directory."""
        all_selected = True
        any_selected = False
        
        # Check current state
        for item in self.files:
            if item == "..":
                continue
                
            item_path = os.path.join(self.current_path, item)
            if not os.path.isdir(item_path):  # Only consider files
                if item_path in self.selected_items:
                    any_selected = True
                    if not self.selected_items[item_path]:
                        all_selected = False
                else:
                    all_selected = False
        
        # Toggle based on current state
        for item in self.files:
            if item == "..":
                continue
                
            item_path = os.path.join(self.current_path, item)
            if not os.path.isdir(item_path):  # Only consider files
                if all_selected:
                    # If all are selected, deselect all
                    if item_path in self.selected_items:
                        del self.selected_items[item_path]
                elif any_selected:
                    # If some are selected, select all
                    self.selected_items[item_path] = True
                else:
                    # If none are selected, select all
                    self.selected_items[item_path] = True
    
    def _handle_key(self, key, stdscr) -> bool:
        """Responds to your keyboard input.
        
        Returns:
            True to keep going, False to exit
        """
        if key == curses.KEY_UP:
            self.cursor_pos = max(0, self.cursor_pos - 1)
        elif key == curses.KEY_DOWN:
            self.cursor_pos = min(len(self.files) - 1, self.cursor_pos + 1)
        elif key == ord('\n'):  # Enter key
            # Get current item
            if not self.files:
                return True
                
            item = self.files[self.cursor_pos]
            item_path = os.path.join(self.current_path, item)
            
            # Handle directory navigation
            if os.path.isdir(item_path):
                if item == "..":
                    # Go up to parent directory
                    self.current_path = os.path.dirname(os.path.abspath(self.current_path))
                else:
                    # Enter the directory
                    self.current_path = item_path
                self.cursor_pos = 0
                self.offset = 0
            else:
                # Toggle selection for files
                self._toggle_selection(item_path)
        elif key == ord(' '):  # Space key
            # Toggle selection state
            if not self.files:
                return True
                
            item = self.files[self.cursor_pos]
            item_path = os.path.join(self.current_path, item)
            self._toggle_selection(item_path)
        elif key == ord('a') or key == ord('A'):
            # Toggle all files in current directory
            self._toggle_all_in_directory()
        elif key == ord('t') or key == ord('T'):
            # Toggle showing hidden files
            self.show_hidden = not self.show_hidden
            self.cursor_pos = 0
            self.offset = 0
        elif key == ord('q') or key == ord('Q'):
            # Quit without saving
            self.save_selections = False
            self.status_message = "Exiting without saving selections"
            return False
        elif key == ord('s') or key == ord('S'):
            # Save and exit
            self.save_selections = True
            self.status_message = "Selections saved!"
            return False
            
        return True
    
    def get_selections(self) -> Tuple[Set[str], Set[str], bool]:
        """Gives you the final list of what's included and excluded.
        
        Returns:
            - Set of files to include
            - Set of directories to exclude
            - Whether to save these choices (True) or discard them (False)
        """
        include_files = {path for path, include in self.selected_items.items() if include}
        exclude_files = {path for path, include in self.selected_items.items() if not include}
        
        # For API consistency with the rest of the program, return paths relative to the starting directory
        relative_include_files = set()
        for path in include_files:
            try:
                rel_path = os.path.relpath(path, self.start_path)
                relative_include_files.add(rel_path)
            except ValueError:
                # Skip paths that can't be made relative (e.g. on different drives in Windows)
                pass
                
        # For directories, we keep absolute paths to match the program's expectations
        return relative_include_files, self.exclude_dirs, self.save_selections
    
    def run(self, stdscr) -> Tuple[Set[str], Set[str], bool]:
        """Starts up the file selector interface.
        
        Args:
            stdscr: The main screen object from curses
            
        Returns:
            - Set of files to include
            - Set of directories to exclude
            - Whether to save these choices
        """
        # Configure curses
        curses.curs_set(0)  # Hide cursor
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)  # Green for included
        curses.init_pair(2, curses.COLOR_RED, -1)    # Red for excluded
        
        # Main loop
        while True:
            self._draw_screen(stdscr)
            key = stdscr.getch()
            if not self._handle_key(key, stdscr):
                break
                
        return self.get_selections()


def select_files_interactive(directory: str) -> Tuple[Set[str], Set[str], bool]:
    """Lets you pick files using an interactive menu.
    
    Args:
        directory: Where to start browsing
        
    Returns:
        - Set of files you want to include
        - Set of directories you want to skip
        - Whether you want to save these choices
    """
    try:
        return curses.wrapper(FileSelector(directory).run)
    except Exception as e:
        print(f"Error in interactive mode: {e}", file=sys.stderr)
        return set(), set(), False
