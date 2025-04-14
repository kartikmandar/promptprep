.. _api_tui:

TUI Module
=========

The ``tui`` module provides the Terminal User Interface for interactive file selection in promptprep.

Module Overview
-------------

.. py:module:: promptprep.tui

The TUI module provides functionality for:

- Displaying a terminal-based file browser
- Allowing users to navigate through directories
- Selecting and deselecting files
- Handling keyboard input
- Managing the visual representation of the file tree

Key Classes and Functions
-----------------------

run_interactive_selection
~~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: run_interactive_selection(directory='.', exclude_dirs=None, extensions=None)

   Run the interactive file selection interface.
   
   :param str directory: The root directory to start from (default: current directory)
   :param list exclude_dirs: List of directories to exclude (default: None)
   :param list extensions: List of file extensions to include (default: None)
   :return: List of selected file paths
   :rtype: list

FileSelector
~~~~~~~~~~

.. py:class:: FileSelector(directory='.', exclude_dirs=None, extensions=None)

   Class for handling interactive file selection.
   
   :param str directory: The root directory to start from (default: current directory)
   :param list exclude_dirs: List of directories to exclude (default: None)
   :param list extensions: List of file extensions to include (default: None)

   .. py:method:: run()

      Run the interactive selection interface.
      
      :return: List of selected file paths
      :rtype: list

   .. py:method:: scan_directory(directory)

      Scan a directory for files and subdirectories.
      
      :param str directory: Directory to scan
      :return: Tuple of (files, subdirectories)
      :rtype: tuple

   .. py:method:: should_include_file(file_path)

      Determine if a file should be included based on extension filters.
      
      :param str file_path: Path to the file
      :return: Whether the file should be included
      :rtype: bool

   .. py:method:: should_exclude_directory(directory)

      Determine if a directory should be excluded.
      
      :param str directory: Directory path
      :return: Whether the directory should be excluded
      :rtype: bool

   .. py:method:: build_file_tree()

      Build the file tree data structure.
      
      :return: Root node of the file tree
      :rtype: TreeNode

   .. py:method:: render_tree()

      Render the file tree to the terminal.
      
      :return: None

   .. py:method:: handle_input()

      Handle keyboard input.
      
      :return: Whether to continue running the interface
      :rtype: bool

   .. py:method:: move_cursor_up()

      Move the cursor up in the file tree.
      
      :return: None

   .. py:method:: move_cursor_down()

      Move the cursor down in the file tree.
      
      :return: None

   .. py:method:: toggle_current_node()

      Toggle selection of the current node.
      
      :return: None

   .. py:method:: toggle_directory_expansion()

      Toggle expansion of the current directory.
      
      :return: None

   .. py:method:: select_all_in_current_directory()

      Select all files in the current directory.
      
      :return: None

   .. py:method:: select_all()

      Select all files in all directories.
      
      :return: None

   .. py:method:: deselect_all_in_current_directory()

      Deselect all files in the current directory.
      
      :return: None

   .. py:method:: deselect_all()

      Deselect all files in all directories.
      
      :return: None

   .. py:method:: toggle_hidden_files()

      Toggle showing hidden files.
      
      :return: None

   .. py:method:: get_selected_files()

      Get the list of selected file paths.
      
      :return: List of selected file paths
      :rtype: list

TreeNode
~~~~~~~

.. py:class:: TreeNode(path, is_dir=False, parent=None)

   Class representing a node in the file tree.
   
   :param str path: Path to the file or directory
   :param bool is_dir: Whether the node is a directory (default: False)
   :param TreeNode parent: Parent node (default: None)

   .. py:attribute:: path

      Path to the file or directory.

   .. py:attribute:: is_dir

      Whether the node is a directory.

   .. py:attribute:: parent

      Parent node.

   .. py:attribute:: children

      List of child nodes.

   .. py:attribute:: is_expanded

      Whether the directory is expanded.

   .. py:attribute:: is_selected

      Whether the file is selected.

   .. py:method:: add_child(child)

      Add a child node.
      
      :param TreeNode child: Child node to add
      :return: None

   .. py:method:: toggle_selection()

      Toggle selection of the node.
      
      :return: None

   .. py:method:: toggle_expansion()

      Toggle expansion of the directory.
      
      :return: None

   .. py:method:: get_display_name()

      Get the display name of the node.
      
      :return: Display name
      :rtype: str

   .. py:method:: get_indent_level()

      Get the indent level of the node.
      
      :return: Indent level
      :rtype: int

   .. py:method:: is_hidden()

      Check if the node is a hidden file or directory.
      
      :return: Whether the node is hidden
      :rtype: bool

TerminalUI
~~~~~~~~~

.. py:class:: TerminalUI

   Class for handling terminal UI operations.

   .. py:method:: init_terminal()

      Initialize the terminal for UI operations.
      
      :return: None

   .. py:method:: restore_terminal()

      Restore the terminal to its original state.
      
      :return: None

   .. py:method:: clear_screen()

      Clear the terminal screen.
      
      :return: None

   .. py:method:: move_cursor(row, col)

      Move the cursor to a specific position.
      
      :param int row: Row position
      :param int col: Column position
      :return: None

   .. py:method:: get_terminal_size()

      Get the size of the terminal.
      
      :return: Tuple of (rows, columns)
      :rtype: tuple

   .. py:method:: read_key()

      Read a key press from the terminal.
      
      :return: Key code
      :rtype: str

   .. py:method:: hide_cursor()

      Hide the terminal cursor.
      
      :return: None

   .. py:method:: show_cursor()

      Show the terminal cursor.
      
      :return: None

Usage Examples
------------

Basic Usage
~~~~~~~~~~

.. code-block:: python

   from promptprep.tui import run_interactive_selection

   # Run interactive selection
   selected_files = run_interactive_selection(
       directory='./my_project',
       exclude_dirs=['node_modules', 'venv'],
       extensions=['.py', '.js']
   )

   # Print selected files
   print("Selected files:")
   for file in selected_files:
       print(f"- {file}")

Custom File Selector
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from promptprep.tui import FileSelector

   # Create a custom file selector
   selector = FileSelector(
       directory='./my_project',
       exclude_dirs=['node_modules', 'venv'],
       extensions=['.py', '.js']
   )

   # Run the selector
   selected_files = selector.run()

   # Process selected files
   print(f"Selected {len(selected_files)} files")

Working with Tree Nodes
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from promptprep.tui import TreeNode

   # Create a file tree manually
   root = TreeNode('project', is_dir=True)
   src = TreeNode('project/src', is_dir=True, parent=root)
   main = TreeNode('project/src/main.py', parent=src)
   utils = TreeNode('project/src/utils.py', parent=src)
   
   # Add children
   root.add_child(src)
   src.add_child(main)
   src.add_child(utils)
   
   # Expand directories
   root.toggle_expansion()  # Expand root
   src.toggle_expansion()   # Expand src
   
   # Select files
   main.toggle_selection()  # Select main.py
   
   # Print tree structure
   def print_tree(node, indent=0):
       prefix = '  ' * indent
       expanded = '[+]' if node.is_dir and node.is_expanded else '[>]' if node.is_dir else '   '
       selected = '[x]' if node.is_selected else '[ ]'
       print(f"{prefix}{expanded} {selected} {node.get_display_name()}")
       if node.is_dir and node.is_expanded:
           for child in node.children:
               print_tree(child, indent + 1)
   
   print_tree(root)

Custom Terminal UI
~~~~~~~~~~~~~~~~

.. code-block:: python

   from promptprep.tui import TerminalUI

   # Create a terminal UI
   ui = TerminalUI()
   
   try:
       # Initialize terminal
       ui.init_terminal()
       ui.hide_cursor()
       
       # Clear screen
       ui.clear_screen()
       
       # Display some text
       ui.move_cursor(0, 0)
       print("Welcome to the file selector!")
       ui.move_cursor(2, 0)
       print("Press any key to continue...")
       
       # Wait for key press
       key = ui.read_key()
       
       # Display pressed key
       ui.move_cursor(4, 0)
       print(f"You pressed: {key}")
       
       # Get terminal size
       rows, cols = ui.get_terminal_size()
       ui.move_cursor(6, 0)
       print(f"Terminal size: {rows} rows x {cols} columns")
       
       # Wait for another key press
       ui.move_cursor(8, 0)
       print("Press any key to exit...")
       ui.read_key()
       
   finally:
       # Restore terminal
       ui.show_cursor()
       ui.restore_terminal()