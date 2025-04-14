.. _usage:

Usage Guide
==========

This guide provides detailed information on how to use promptprep effectively.

Basic Command Structure
----------------------

The basic command structure for promptprep is:

.. code-block:: bash

   promptprep [options]

When run without any options, promptprep will:

1. Scan the current directory for code files
2. Generate an ASCII directory tree
3. Aggregate the content of all code files
4. Save the result to ``full_code.txt``

Core Options
-----------

Directory Selection
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep -d PATH, --directory PATH

Specify which directory to scan. By default, promptprep uses the current directory.

Output Options
~~~~~~~~~~~~~

.. code-block:: bash

   promptprep -o FILE, --output-file FILE

Specify where to save the output. By default, promptprep saves to ``full_code.txt``.

.. code-block:: bash

   promptprep -c, --clipboard

Send the output directly to the clipboard instead of saving to a file.

File Selection and Filtering
---------------------------

Include Specific Files
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep -i LIST, --include-files LIST

Only process the specified files. Provide a comma-separated list of relative paths.

Example:

.. code-block:: bash

   promptprep -i "src/main.py,src/utils.py,README.md"

Exclude Directories
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep -e LIST, --exclude-dirs LIST

Skip the specified directories. Provide a comma-separated list of directory names.

Example:

.. code-block:: bash

   promptprep -e "node_modules,venv,.git,__pycache__"

Filter by Extension
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep -x LIST, --extensions LIST

Only include files with the specified extensions. Provide a comma-separated list of extensions.

Example:

.. code-block:: bash

   promptprep -x ".py,.js,.md"

Maximum File Size
~~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep -m SIZE, --max-file-size SIZE

Skip files larger than the specified size in MB. Default is 100.0 MB.

Example:

.. code-block:: bash

   promptprep -m 5  # Skip files larger than 5 MB

Interactive Mode
~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep --interactive

Launch a terminal-based file browser to select files visually.

Content Processing Options
-------------------------

Summary Mode
~~~~~~~~~~~

.. code-block:: bash

   promptprep --summary-mode

Extract only function/class signatures and docstrings, skipping implementation details.

Comment Control
~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep --include-comments  # Default behavior
   promptprep --no-include-comments  # Strip all comments

Control whether comments are included in the output.

Metadata
~~~~~~~

.. code-block:: bash

   promptprep --metadata

Add statistics about your codebase at the beginning of the output.

Token Counting
~~~~~~~~~~~~~

.. code-block:: bash

   promptprep --count-tokens
   promptprep --token-model MODEL  # Default: cl100k_base (GPT-4)

Count how many tokens your code will use when sent to AI models. Requires ``--metadata``.

Output Formatting
----------------

Format Selection
~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep --format FORMAT

Choose the output format. Available options:

- ``plain``: Simple text format (default)
- ``markdown``: GitHub-friendly Markdown with code blocks
- ``html``: Complete webpage with basic styling
- ``highlighted``: Syntax-highlighted code (requires pygments)
- ``custom``: Custom format using a template file

Line Numbers
~~~~~~~~~~~

.. code-block:: bash

   promptprep --line-numbers

Add line numbers to the code in the output.

Custom Templates
~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep --format custom --template-file FILE

Use a custom template file for the output. See :ref:`custom_templates` for details.

Advanced Features
----------------

Incremental Processing
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep --incremental
   promptprep --last-run-timestamp TIMESTAMP

Only process files that have changed since the last run. See :ref:`incremental_processing` for details.

Diff Generation
~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep --diff PREV_FILE
   promptprep --diff-context LINES  # Default: 3
   promptprep --diff-output FILE

Compare with a previous output file and show what changed. See :ref:`diff_generation` for details.

Configuration Management
-----------------------

Save Configuration
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep [options] --save-config [FILE]

Save the current options to a configuration file for later use.

Load Configuration
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep --load-config [FILE] [additional options]

Load options from a configuration file. Additional options will override the loaded ones.

Examples
-------

Here are some examples of common use cases:

Basic Usage
~~~~~~~~~~

.. code-block:: bash

   # Process current directory, save to output.txt
   promptprep -o output.txt

   # Process a specific project, format as markdown
   promptprep -d ./my_project -o project_code.md --format markdown

   # Copy to clipboard instead of saving to file
   promptprep -c

File Selection
~~~~~~~~~~~~~

.. code-block:: bash

   # Only include Python files
   promptprep -x ".py" -o python_code.txt

   # Exclude test directories and virtual environments
   promptprep -e "tests,venv,__pycache__" -o app_code.txt

   # Select files interactively
   promptprep --interactive -c

Content Processing
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Get a high-level overview with stats
   promptprep --summary-mode --metadata -o summary.txt

   # Strip comments for a cleaner output
   promptprep --no-include-comments -o clean_code.txt

   # Count tokens for AI model context limits
   promptprep --metadata --count-tokens -o tokenized.txt

Output Formatting
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Create a pretty HTML report with syntax highlighting
   promptprep --format highlighted -o report.html

   # Generate markdown with line numbers
   promptprep --format markdown --line-numbers -o code_with_lines.md

Advanced Usage
~~~~~~~~~~~~~

.. code-block:: bash

   # Only process files changed since last run
   promptprep --incremental -o updated_code.txt

   # Compare with previous version
   promptprep --diff previous_code.txt -o diff_report.txt

   # Save your favorite settings
   promptprep -d ./src -x ".py,.js" -e "node_modules" --format markdown --save-config my_settings.json

   # Use saved settings
   promptprep --load-config my_settings.json -o new_output.md