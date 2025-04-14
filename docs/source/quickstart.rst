.. _quickstart:

Quickstart
=========

This guide will help you get up and running with promptprep quickly.

Basic Usage
----------

After :ref:`installation`, you can start using promptprep right away. The simplest command is:

.. code-block:: bash

   promptprep

This will scan your current directory for code files, create an ASCII directory tree, and save the aggregated code to ``full_code.txt``.

Common Scenarios
---------------

Here are some common use cases to get you started:

Preparing Code for AI Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you need to share your code with AI models like GPT-4:

.. code-block:: bash

   promptprep -d ./my_project --format markdown -c

This command:

- Scans the ``./my_project`` directory
- Formats the output as Markdown (great for AI models)
- Copies the result to your clipboard (``-c``) for easy pasting

Creating a Project Snapshot
~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a comprehensive snapshot of your project:

.. code-block:: bash

   promptprep -d ./src --metadata --count-tokens -o project_snapshot.md --format markdown

This command:

- Scans the ``./src`` directory
- Adds metadata about your codebase
- Counts tokens (useful for AI model context limits)
- Saves the output as Markdown to ``project_snapshot.md``

Focusing on Specific Files
~~~~~~~~~~~~~~~~~~~~~~~~~

To include only certain file types:

.. code-block:: bash

   promptprep -x ".py,.js" -e "node_modules,venv" -o code_selection.txt

This command:

- Only includes Python and JavaScript files (``.py``, ``.js``)
- Excludes the ``node_modules`` and ``venv`` directories
- Saves the output to ``code_selection.txt``

Interactive Selection
~~~~~~~~~~~~~~~~~~~~

For a visual way to select files:

.. code-block:: bash

   promptprep --interactive -c

This launches a terminal-based file browser where you can:

- Navigate with arrow keys
- Select/deselect files with Space or Enter
- Press ``a`` to select all files in a directory
- Press ``s`` to save your selection and continue
- Press ``q`` to quit

The result will be copied to your clipboard.

Next Steps
---------

Now that you've seen the basics, you can:

- Explore the :ref:`usage` page for more detailed information
- Check out the :ref:`command_reference` for all available options
- Learn about :ref:`output_formats` to customize your output
- See :ref:`examples` for more real-world use cases

.. tip::
   Save your favorite command options with ``--save-config`` to avoid typing them repeatedly. Later, use ``--load-config`` to apply those saved settings.