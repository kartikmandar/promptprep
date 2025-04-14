.. _api_cli:

CLI Module
=========

The ``cli`` module provides the command-line interface for promptprep.

Module Overview
-------------

.. py:module:: promptprep.cli

The CLI module provides functionality for:

- Parsing command-line arguments
- Executing the main functionality of promptprep
- Handling configuration loading and saving
- Managing clipboard operations
- Coordinating between different components

Key Functions
-----------

main
~~~~

.. py:function:: main()

   The main entry point for the promptprep command-line tool.
   
   This function:
   
   1. Parses command-line arguments
   2. Loads configuration if requested
   3. Creates a CodeAggregator instance
   4. Processes the code
   5. Formats the output
   6. Saves the output or copies it to the clipboard
   
   :return: Exit code (0 for success, non-zero for failure)
   :rtype: int

parse_args
~~~~~~~~~

.. py:function:: parse_args(args=None)

   Parse command-line arguments.
   
   :param list args: Command-line arguments (default: None, which uses sys.argv)
   :return: Parsed arguments
   :rtype: argparse.Namespace

load_config
~~~~~~~~~~

.. py:function:: load_config(config_file=None)

   Load configuration from a file.
   
   :param str config_file: Path to the configuration file (default: None, which uses the default location)
   :return: Loaded configuration as a dictionary
   :rtype: dict
   :raises FileNotFoundError: If the configuration file doesn't exist

save_config
~~~~~~~~~~

.. py:function:: save_config(args, config_file=None)

   Save configuration to a file.
   
   :param argparse.Namespace args: Command-line arguments
   :param str config_file: Path to the configuration file (default: None, which uses the default location)
   :return: None

get_default_config_path
~~~~~~~~~~~~~~~~~~~~~

.. py:function:: get_default_config_path()

   Get the default path for the configuration file.
   
   :return: Default configuration file path
   :rtype: str

args_to_dict
~~~~~~~~~~~

.. py:function:: args_to_dict(args)

   Convert command-line arguments to a dictionary.
   
   :param argparse.Namespace args: Command-line arguments
   :return: Arguments as a dictionary
   :rtype: dict

dict_to_args
~~~~~~~~~~~

.. py:function:: dict_to_args(config_dict, parser)

   Convert a configuration dictionary to command-line arguments.
   
   :param dict config_dict: Configuration dictionary
   :param argparse.ArgumentParser parser: Argument parser
   :return: Updated command-line arguments
   :rtype: argparse.Namespace

copy_to_clipboard
~~~~~~~~~~~~~~~

.. py:function:: copy_to_clipboard(content)

   Copy content to the system clipboard.
   
   :param str content: Content to copy to the clipboard
   :return: None
   :raises ImportError: If pyperclip is not installed

process_code
~~~~~~~~~~

.. py:function:: process_code(args)

   Process code based on the provided arguments.
   
   :param argparse.Namespace args: Command-line arguments
   :return: Processed code content
   :rtype: str

format_output
~~~~~~~~~~~

.. py:function:: format_output(content, args)

   Format the output based on the specified format.
   
   :param str content: Content to format
   :param argparse.Namespace args: Command-line arguments
   :return: Formatted content
   :rtype: str

handle_output
~~~~~~~~~~~

.. py:function:: handle_output(content, args)

   Handle the output (save to file or copy to clipboard).
   
   :param str content: Content to output
   :param argparse.Namespace args: Command-line arguments
   :return: None

Command-Line Arguments
--------------------

The CLI module defines the following command-line arguments:

Core Options
~~~~~~~~~~~

- ``-d, --directory``: Directory to scan for code files (default: current directory)
- ``-o, --output-file``: Output file path (default: 'full_code.txt')
- ``-c, --clipboard``: Copy output to clipboard instead of saving to a file

File Selection Options
~~~~~~~~~~~~~~~~~~~~

- ``-i, --include-files``: Only include these specific files (comma-separated list)
- ``-e, --exclude-dirs``: Skip these directories (comma-separated list)
- ``-x, --extensions``: Only include files with these extensions (comma-separated list)
- ``-m, --max-file-size``: Skip files larger than this size in MB (default: 100.0)
- ``--interactive``: Launch terminal-based file browser for visual selection

Content Processing Options
~~~~~~~~~~~~~~~~~~~~~~~~

- ``--summary-mode``: Extract only function/class signatures and docstrings
- ``--include-comments``: Include comments in the output (default: True)
- ``--no-include-comments``: Strip all comments from the output
- ``--metadata``: Add statistics about your codebase at the beginning
- ``--count-tokens``: Count tokens for AI model context limits (requires ``--metadata``)
- ``--token-model``: Tokenizer model to use (default: 'cl100k_base' for GPT-4)

Output Formatting Options
~~~~~~~~~~~~~~~~~~~~~~~

- ``--format``: Output format: 'plain', 'markdown', 'html', 'highlighted', or 'custom'
- ``--line-numbers``: Add line numbers to code in the output
- ``--template-file``: Custom template file (required if using ``--format custom``)

Incremental Processing Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``--incremental``: Only process files that have changed since last run
- ``--last-run-timestamp``: Unix timestamp of last run

Diff Generation Options
~~~~~~~~~~~~~~~~~~~~~

- ``--diff``: Compare with a previous output file and show changes
- ``--diff-context``: Number of unchanged lines to show around changes (default: 3)
- ``--diff-output``: Save diff to a file instead of showing on screen

Configuration Management Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``--save-config``: Save current options to a configuration file
- ``--load-config``: Load options from a configuration file

Other Options
~~~~~~~~~~~

- ``--version``: Show version number and exit
- ``-h, --help``: Show help message and exit

Usage Examples
------------

Basic Usage
~~~~~~~~~~

.. code-block:: python

   from promptprep.cli import main

   # Run the CLI with default arguments
   exit_code = main()

Custom Arguments
~~~~~~~~~~~~~~

.. code-block:: python

   import sys
   from promptprep.cli import main

   # Set custom arguments
   sys.argv = ['promptprep', '-d', './my_project', '-o', 'output.md', '--format', 'markdown']

   # Run the CLI with custom arguments
   exit_code = main()

Programmatic Usage
~~~~~~~~~~~~~~~~

.. code-block:: python

   from promptprep.cli import parse_args, process_code, format_output, handle_output

   # Parse arguments
   args = parse_args(['-d', './my_project', '-o', 'output.md', '--format', 'markdown'])

   # Process code
   content = process_code(args)

   # Format output
   formatted_content = format_output(content, args)

   # Handle output
   handle_output(formatted_content, args)

Configuration Management
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from promptprep.cli import parse_args, load_config, save_config, get_default_config_path

   # Save configuration
   args = parse_args(['-d', './my_project', '--format', 'markdown'])
   save_config(args)

   # Load configuration
   config = load_config()
   print(f"Loaded configuration: {config}")

   # Get default config path
   config_path = get_default_config_path()
   print(f"Default configuration path: {config_path}")

Clipboard Operations
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from promptprep.cli import copy_to_clipboard

   # Copy content to clipboard
   content = "This is some content to copy to the clipboard."
   copy_to_clipboard(content)
   print("Content copied to clipboard!")