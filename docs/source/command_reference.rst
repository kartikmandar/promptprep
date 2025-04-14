.. _command_reference:

Command Reference
================

This page provides a comprehensive reference for all command-line options available in promptprep.

Core Options
-----------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Option
     - Description
   * - ``-d PATH, --directory PATH``
     - Directory to scan for code files (default: current directory)
   * - ``-o FILE, --output-file FILE``
     - Output file path (default: ``full_code.txt``)
   * - ``-c, --clipboard``
     - Copy output to clipboard instead of saving to a file

File Selection Options
---------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Option
     - Description
   * - ``-i LIST, --include-files LIST``
     - Only include these specific files (comma-separated list of relative paths)
   * - ``-e LIST, --exclude-dirs LIST``
     - Skip these directories (comma-separated list)
   * - ``-x LIST, --extensions LIST``
     - Only include files with these extensions (comma-separated list)
   * - ``-m SIZE, --max-file-size SIZE``
     - Skip files larger than this size in MB (default: 100.0)
   * - ``--interactive``
     - Launch terminal-based file browser for visual selection

Content Processing Options
-------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Option
     - Description
   * - ``--summary-mode``
     - Extract only function/class signatures and docstrings
   * - ``--include-comments``
     - Include comments in the output (default)
   * - ``--no-include-comments``
     - Strip all comments from the output
   * - ``--metadata``
     - Add statistics about your codebase at the beginning
   * - ``--count-tokens``
     - Count tokens for AI model context limits (requires ``--metadata``)
   * - ``--token-model MODEL``
     - Tokenizer model to use (default: ``cl100k_base`` for GPT-4)

Output Formatting Options
------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Option
     - Description
   * - ``--format FORMAT``
     - Output format: ``plain``, ``markdown``, ``html``, ``highlighted``, or ``custom``
   * - ``--line-numbers``
     - Add line numbers to code in the output
   * - ``--template-file FILE``
     - Custom template file (required if using ``--format custom``)

Incremental Processing Options
-----------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Option
     - Description
   * - ``--incremental``
     - Only process files that have changed since last run
   * - ``--last-run-timestamp TS``
     - Unix timestamp of last run (e.g., ``1678886400.0``)

Diff Generation Options
----------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Option
     - Description
   * - ``--diff PREV_FILE``
     - Compare with a previous output file and show changes
   * - ``--diff-context LINES``
     - Number of unchanged lines to show around changes (default: 3)
   * - ``--diff-output FILE``
     - Save diff to a file instead of showing on screen

Configuration Management Options
------------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Option
     - Description
   * - ``--save-config [FILE]``
     - Save current options to a configuration file
   * - ``--load-config [FILE]``
     - Load options from a configuration file

Other Options
------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Option
     - Description
   * - ``--version``
     - Show version number and exit
   * - ``-h, --help``
     - Show help message and exit

Option Details
-------------

Directory Selection
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep -d PATH, --directory PATH

Specify the directory to scan for code files. If not provided, promptprep will use the current directory.

Output Options
~~~~~~~~~~~~~

.. code-block:: bash

   promptprep -o FILE, --output-file FILE

Specify the file where the output should be saved. If not provided, promptprep will save to ``full_code.txt``.

.. code-block:: bash

   promptprep -c, --clipboard

Send the output directly to the clipboard instead of saving to a file. This is useful when you want to immediately paste the output into another application.

File Selection
~~~~~~~~~~~~~

.. code-block:: bash

   promptprep -i LIST, --include-files LIST

Only process the specified files. Provide a comma-separated list of relative paths. For example:

.. code-block:: bash

   promptprep -i "src/main.py,src/utils.py,README.md"

.. code-block:: bash

   promptprep -e LIST, --exclude-dirs LIST

Skip the specified directories. Provide a comma-separated list of directory names. For example:

.. code-block:: bash

   promptprep -e "node_modules,venv,.git,__pycache__"

.. code-block:: bash

   promptprep -x LIST, --extensions LIST

Only include files with the specified extensions. Provide a comma-separated list of extensions. For example:

.. code-block:: bash

   promptprep -x ".py,.js,.md"

.. code-block:: bash

   promptprep -m SIZE, --max-file-size SIZE

Skip files larger than the specified size in MB. Default is 100.0 MB. For example:

.. code-block:: bash

   promptprep -m 5  # Skip files larger than 5 MB

.. code-block:: bash

   promptprep --interactive

Launch a terminal-based file browser to select files visually.

Content Processing
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep --summary-mode

Extract only function/class signatures and docstrings, skipping implementation details.

.. code-block:: bash

   promptprep --include-comments  # Default behavior
   promptprep --no-include-comments  # Strip all comments

Control whether comments are included in the output.

.. code-block:: bash

   promptprep --metadata

Add statistics about your codebase at the beginning of the output.

.. code-block:: bash

   promptprep --count-tokens
   promptprep --token-model MODEL  # Default: cl100k_base (GPT-4)

Count how many tokens your code will use when sent to AI models. Requires ``--metadata``.

Output Formatting
~~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep --format FORMAT

Choose the output format. Available options:

- ``plain``: Simple text format (default)
- ``markdown``: GitHub-friendly Markdown with code blocks
- ``html``: Complete webpage with basic styling
- ``highlighted``: Syntax-highlighted code (requires pygments)
- ``custom``: Custom format using a template file

.. code-block:: bash

   promptprep --line-numbers

Add line numbers to the code in the output.

.. code-block:: bash

   promptprep --format custom --template-file FILE

Use a custom template file for the output.

Incremental Processing
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep --incremental
   promptprep --last-run-timestamp TIMESTAMP

Only process files that have changed since the last run.

Diff Generation
~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep --diff PREV_FILE
   promptprep --diff-context LINES  # Default: 3
   promptprep --diff-output FILE

Compare with a previous output file and show what changed.

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep [options] --save-config [FILE]

Save the current options to a configuration file for later use.

.. code-block:: bash

   promptprep --load-config [FILE] [additional options]

Load options from a configuration file. Additional options will override the loaded ones.