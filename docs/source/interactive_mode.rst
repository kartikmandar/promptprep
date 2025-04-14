.. _interactive_mode:

Interactive Mode
===============

Interactive mode provides a visual, terminal-based interface for selecting which files to include in your output. This is particularly useful when you want to cherry-pick specific files without typing long paths.

Overview
--------

When you run promptprep with the ``--interactive`` option, it will:

1. Launch a terminal-based file browser
2. Allow you to navigate through your project's directory structure
3. Let you select or deselect individual files
4. Process only the files you've selected

This provides a more intuitive way to select files compared to listing them manually with the ``-i, --include-files`` option.

Basic Usage
----------

To use interactive mode:

.. code-block:: bash

   promptprep --interactive [other options]

Example:

.. code-block:: bash

   promptprep --interactive -o selected_files.txt

This will launch the interactive file browser, let you select files, and then save the output to ``selected_files.txt``.

Navigation Controls
------------------

Once in the interactive mode, you can use the following controls:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Key
     - Action
   * - **↑/↓ Arrow Keys**
     - Navigate up and down through files and directories
   * - **Enter** or **Space**
     - Select/deselect the current file or toggle directory expansion
   * - **→ Arrow Key**
     - Expand a directory
   * - **← Arrow Key**
     - Collapse a directory
   * - **a**
     - Select all files in the current directory
   * - **A**
     - Select all files in all directories
   * - **n**
     - Deselect all files in the current directory
   * - **N**
     - Deselect all files in all directories
   * - **t**
     - Toggle showing hidden files (those starting with a dot)
   * - **s**
     - Save your selection and continue processing
   * - **q**
     - Quit without processing (cancel)

Visual Indicators
----------------

The interactive browser uses visual indicators to show the status of files and directories:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Indicator
     - Meaning
   * - **[ ]**
     - Unselected file
   * - **[x]**
     - Selected file
   * - **[+]**
     - Expanded directory
   * - **[>]**
     - Collapsed directory
   * - **[.]**
     - Hidden file or directory (when hidden files are shown)

Example Session
--------------

Here's what a typical interactive session might look like:

.. code-block:: text

    Select files to include (navigate with arrow keys, select with space/enter):
    
    [+] project/
      [+] src/
        [ ] main.py
        [x] utils.py
        [ ] config.py
      [+] tests/
        [ ] test_main.py
        [ ] test_utils.py
      [ ] README.md
      [x] LICENSE
    
    Selected: 2 files
    Press 's' to save selection and continue, 'q' to quit

In this example, ``utils.py`` and ``LICENSE`` have been selected for processing.

Combining with Other Features
----------------------------

Interactive mode works well with other promptprep features:

With Output Formatting
~~~~~~~~~~~~~~~~~~~~~

Select files visually and format the output as needed:

.. code-block:: bash

   promptprep --interactive --format markdown -o selected.md

With Clipboard Integration
~~~~~~~~~~~~~~~~~~~~~~~~~ 

Select files visually and copy directly to clipboard:

.. code-block:: bash

   promptprep --interactive -c

This is particularly useful for quickly sharing selected code with AI models or colleagues.

Advanced Use Cases
-----------------

Code Reviews
~~~~~~~~~~~

Select specific files for a code review:

.. code-block:: bash

   promptprep --interactive --format highlighted -o review.html

This lets you visually select the files you want to review and creates a syntax-highlighted HTML file.

Focused AI Assistance
~~~~~~~~~~~~~~~~~~~~

When seeking help from AI models for specific parts of your codebase:

.. code-block:: bash

   promptprep --interactive --format markdown --metadata --count-tokens -c

This lets you select only the relevant files, adds metadata with token count, and copies to clipboard for pasting into an AI chat.

Teaching and Presentations
~~~~~~~~~~~~~~~~~~~~~~~~~

When preparing code examples for teaching or presentations:

.. code-block:: bash

   promptprep --interactive --summary-mode --format markdown -o teaching_examples.md

This lets you select specific files and extract only the function/class signatures and docstrings.

Best Practices
-------------

1. **Start with a Clear Goal**: Know what files you're looking for before starting the interactive session.

2. **Use Directory Selection**: Select or deselect entire directories when appropriate to save time.

3. **Check Your Selection**: Review the "Selected: X files" counter before saving to ensure you've selected what you intended.

4. **Combine with Filters**: Use ``-x, --extensions`` and ``-e, --exclude-dirs`` to pre-filter files before the interactive selection.

5. **Save Configurations**: If you frequently select the same files, consider saving your selection as a configuration file.

Troubleshooting
--------------

If interactive mode isn't working as expected:

1. **Terminal Compatibility**: Ensure your terminal supports the required features (most modern terminals do).

2. **Window Size**: Make sure your terminal window is large enough to display the file browser properly.

3. **Color Support**: If colors aren't displaying correctly, check your terminal's color support.

4. **Navigation Issues**: If navigation is difficult, try using the arrow keys instead of Enter/Space for navigation.

Limitations
----------

There are some limitations to be aware of:

1. **Large Directory Trees**: Very large directory trees might be cumbersome to navigate.

2. **Terminal Dependency**: Interactive mode requires a compatible terminal and might not work in all environments.

3. **No Search**: Currently, there's no search functionality within the interactive browser.

4. **No Multi-Select**: You can't select multiple non-contiguous files in a single action (though you can select all in a directory).