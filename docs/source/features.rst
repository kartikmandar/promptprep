.. _features:

Features
========

promptprep offers a rich set of features designed to make code aggregation and sharing as flexible and powerful as possible.

Core Features
------------

Code Aggregation
~~~~~~~~~~~~~~~

The primary function of promptprep is to combine multiple source files into a single, well-organized output file. This makes it easy to:

- Share your code with AI models like GPT-4
- Create documentation snapshots
- Analyze your codebase
- Facilitate code reviews

Directory Tree Visualization
~~~~~~~~~~~~~~~~~~~~~~~~~~~

promptprep generates an ASCII directory tree that provides a visual map of your project structure:

.. code-block:: text

    project/
    ├── src/
    │   ├── main.py
    │   └── utils.py
    └── tests/
        └── test_main.py

This helps readers understand how your files are organized and relate to each other.

Smart File Selection
-------------------

Include/Exclude Patterns
~~~~~~~~~~~~~~~~~~~~~~~

Control exactly which files are processed:

- Include specific files with ``-i, --include-files``
- Exclude directories with ``-e, --exclude-dirs``
- Filter by file extension with ``-x, --extensions``

Size Limits
~~~~~~~~~~

Skip files that are too large to be useful with the ``-m, --max-file-size`` option. This prevents your output from being bloated with large binary files or data dumps.

Interactive Selection
~~~~~~~~~~~~~~~~~~~

The ``--interactive`` option launches a terminal-based file browser that lets you visually select which files to include:

- Navigate with arrow keys
- Select/deselect with Space or Enter
- Select all files in a directory with ``a``
- Save selection with ``s``
- Quit with ``q``

Content Processing
-----------------

Summary Mode
~~~~~~~~~~~

The ``--summary-mode`` option extracts only function/class signatures and docstrings, skipping implementation details. This is perfect for getting a high-level overview of a codebase.

Comment Control
~~~~~~~~~~~~~~

Control whether comments are included in the output:

- ``--include-comments``: Keep comments (default)
- ``--no-include-comments``: Strip all comments

Line Numbers
~~~~~~~~~~~

Add line numbers to the code in the output with the ``--line-numbers`` option. This makes it easier to reference specific parts of the code.

Output Formats
-------------

promptprep supports multiple output formats to suit different needs:

Plain Text
~~~~~~~~~

The default format is plain text, which is simple and works everywhere.

Markdown
~~~~~~~

The ``markdown`` format creates GitHub-friendly output with proper code blocks and syntax highlighting.

HTML
~~~~

The ``html`` format generates a complete webpage with basic styling.

Syntax Highlighting
~~~~~~~~~~~~~~~~~

The ``highlighted`` format adds full syntax highlighting with colors to make your code more readable. This requires the optional ``pygments`` package.

Custom Templates
~~~~~~~~~~~~~~

The ``custom`` format lets you design your own output format using a template file. See :ref:`custom_templates` for details.

Analytics and Metadata
---------------------

Code Statistics
~~~~~~~~~~~~~~

The ``--metadata`` option adds statistics about your codebase at the beginning of the output, including:

- Number of files
- Total lines of code
- Comment ratio
- File size information

Token Counting
~~~~~~~~~~~~~

The ``--count-tokens`` option estimates how many tokens your code will use when sent to AI models like GPT-4. This helps you stay within context limits.

Advanced Features
----------------

Incremental Processing
~~~~~~~~~~~~~~~~~~~~~

The ``--incremental`` option processes only files that have changed since the last run, saving time on large projects.

Diff Generation
~~~~~~~~~~~~~~

The ``--diff`` option compares with a previous output file and shows what changed, making it easy to track changes over time.

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~

Save your favorite command options with ``--save-config`` and load them later with ``--load-config``.

Clipboard Integration
~~~~~~~~~~~~~~~~~~~

The ``-c, --clipboard`` option sends the output directly to your clipboard, ready to paste into your application of choice.

Platform Support
---------------

promptprep works on:

- Windows
- macOS
- Linux

It's compatible with Python 3.7 and higher.