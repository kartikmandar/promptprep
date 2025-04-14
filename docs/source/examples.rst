.. _examples:

Examples
========

This page provides real-world examples of how to use promptprep for different scenarios.

Working with AI Models
---------------------

Preparing Code for GPT-4
~~~~~~~~~~~~~~~~~~~~~~~

When you need to share your code with AI models like GPT-4 for assistance:

.. code-block:: bash

   promptprep -d ./my_project --format markdown --metadata --count-tokens -c

This command:

- Scans the ``./my_project`` directory
- Formats the output as Markdown (great for AI models)
- Adds metadata including token count (helps stay within context limits)
- Copies the result to your clipboard for easy pasting

Focusing on a Specific Issue
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you need help with a specific part of your codebase:

.. code-block:: bash

   promptprep -i "src/problematic_file.py,src/related_file.py" --format markdown -c

This command:

- Only includes the specified files
- Formats the output as Markdown
- Copies the result to your clipboard

Documentation and Sharing
------------------------

Creating a Project Snapshot
~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a comprehensive snapshot of your project for documentation:

.. code-block:: bash

   promptprep -d ./src --metadata --format html -o project_snapshot.html

This command:

- Scans the ``./src`` directory
- Adds metadata about your codebase
- Creates an HTML file with syntax highlighting
- Saves the output to ``project_snapshot.html``

Generating Documentation for a Specific Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To document a specific module or component:

.. code-block:: bash

   promptprep -d ./src/module --summary-mode --format markdown -o module_docs.md

This command:

- Focuses on the ``./src/module`` directory
- Uses summary mode to extract only signatures and docstrings
- Formats the output as Markdown
- Saves the output to ``module_docs.md``

Code Reviews
-----------

Preparing Code for Review
~~~~~~~~~~~~~~~~~~~~~~~

When preparing code for a review:

.. code-block:: bash

   promptprep -d ./feature_branch --diff main_branch_snapshot.txt --format highlighted -o review.html

This command:

- Scans the ``./feature_branch`` directory
- Compares with a previous snapshot of the main branch
- Creates a syntax-highlighted HTML file showing the changes
- Saves the output to ``review.html``

Focusing on Changed Files
~~~~~~~~~~~~~~~~~~~~~~~

To review only files that have changed since a specific time:

.. code-block:: bash

   promptprep --incremental --last-run-timestamp 1678886400.0 --format markdown -o changes.md

This command:

- Only processes files that have changed since the specified timestamp
- Formats the output as Markdown
- Saves the output to ``changes.md``

Project Analysis
--------------

Analyzing Code Metrics
~~~~~~~~~~~~~~~~~~~~

To get statistics about your codebase:

.. code-block:: bash

   promptprep -d . --metadata --no-include-comments -o metrics.txt

This command:

- Scans the current directory
- Adds metadata about your codebase
- Strips comments to focus on actual code
- Saves the output to ``metrics.txt``

Language-Specific Analysis
~~~~~~~~~~~~~~~~~~~~~~~~

To analyze only specific file types:

.. code-block:: bash

   promptprep -d . -x ".py" --metadata --count-tokens -o python_analysis.txt

This command:

- Scans the current directory
- Only includes Python files
- Adds metadata and token count
- Saves the output to ``python_analysis.txt``

Advanced Use Cases
----------------

Custom Output Format
~~~~~~~~~~~~~~~~~~

To create a custom output format:

.. code-block:: bash

   promptprep -d . --format custom --template-file my_template.txt -o custom_output.txt

This command:

- Scans the current directory
- Uses a custom template for formatting
- Saves the output to ``custom_output.txt``

Selective File Processing
~~~~~~~~~~~~~~~~~~~~~~~

To process only specific files and exclude certain directories:

.. code-block:: bash

   promptprep -d . -x ".js,.ts" -e "node_modules,dist,build" -o frontend_code.txt

This command:

- Scans the current directory
- Only includes JavaScript and TypeScript files
- Excludes the ``node_modules``, ``dist``, and ``build`` directories
- Saves the output to ``frontend_code.txt``

Interactive Selection
~~~~~~~~~~~~~~~~~~~

To visually select which files to include:

.. code-block:: bash

   promptprep -d . --interactive -o selected_files.txt

This command:

- Scans the current directory
- Launches a terminal-based file browser for selection
- Saves the output to ``selected_files.txt``

Workflow Integration
------------------

Continuous Integration
~~~~~~~~~~~~~~~~~~~~

To generate code snapshots as part of a CI pipeline:

.. code-block:: bash

   # In your CI script
   promptprep -d . --metadata --format markdown -o snapshot.md
   # Then commit or upload the snapshot

Git Hooks
~~~~~~~~

To create a snapshot before committing changes:

.. code-block:: bash

   # In .git/hooks/pre-commit
   promptprep -d . --incremental --format markdown -o latest_changes.md

Team Collaboration
~~~~~~~~~~~~~~~~

To share consistent code snapshots with team members:

1. Create a team configuration:

   .. code-block:: bash

      promptprep -d . -e "node_modules,venv,__pycache__" --format markdown --save-config team_config.json

2. Share the configuration with team members.

3. Team members can use the configuration:

   .. code-block:: bash

      promptprep --load-config team_config.json -o my_snapshot.md

This ensures everyone uses the same settings when creating snapshots.