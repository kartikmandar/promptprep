promptprep
==========

.. toctree::
   :maxdepth: 4

   promptprep

.. _api_modules:

Modules Overview
==============

promptprep is organized into several modules, each with a specific responsibility. This page provides an overview of these modules and how they interact.

Module Structure
--------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Module
     - Description
   * - :ref:`api_aggregator`
     - Core functionality for scanning, processing, and aggregating code files
   * - :ref:`api_formatters`
     - Output formatting in various formats (plain, markdown, HTML, etc.)
   * - :ref:`api_cli`
     - Command-line interface and argument parsing
   * - :ref:`api_config`
     - Configuration management and persistence
   * - :ref:`api_tui`
     - Terminal user interface for interactive file selection

Module Interactions
-----------------

The modules interact in the following way:

1. The **CLI** module parses command-line arguments and coordinates the overall process.
2. The **Config** module loads and saves configuration settings.
3. The **TUI** module (if interactive mode is enabled) allows the user to select files.
4. The **Aggregator** module scans directories, processes files, and aggregates code.
5. The **Formatters** module formats the aggregated code in the desired output format.

Here's a simplified flow diagram:

.. code-block:: text

    ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
    │   CLI   │────▶│ Config  │     │   TUI   │     │Aggregator│────▶│Formatters│
    └─────────┘     └─────────┘     └─────────┘     └─────────┘     └─────────┘
         │                │               ▲               ▲
         │                │               │               │
         └────────────────┼───────────────┘               │
                          │                               │
                          └───────────────────────────────┘

Module Details
------------

Aggregator Module
~~~~~~~~~~~~~~~

The :ref:`api_aggregator` module is the core of promptprep. It handles:

- Scanning directories for code files
- Filtering files based on various criteria
- Processing file content (with or without comments, summary mode, etc.)
- Generating directory trees
- Incremental processing
- Generating diffs between versions

Formatters Module
~~~~~~~~~~~~~~

The :ref:`api_formatters` module handles the output formatting. It supports:

- Plain text format
- Markdown format with code blocks
- HTML format
- Syntax-highlighted HTML (with Pygments)
- Custom templates

CLI Module
~~~~~~~~

The :ref:`api_cli` module provides the command-line interface. It handles:

- Parsing command-line arguments
- Coordinating the overall process
- Handling clipboard operations
- Error handling and reporting

Config Module
~~~~~~~~~~

The :ref:`api_config` module manages configuration settings. It handles:

- Loading configuration from files
- Saving configuration to files
- Managing default settings
- Converting between configuration formats

TUI Module
~~~~~~~~

The :ref:`api_tui` module provides the interactive file selection interface. It handles:

- Displaying a terminal-based file browser
- Allowing navigation through directories
- Selecting and deselecting files
- Handling keyboard input

Extending promptprep
------------------

If you want to extend promptprep with new features, here are some guidelines:

1. **New Output Format**: Add a new formatter class in the formatters module that inherits from BaseFormatter.

2. **New File Processing Method**: Extend the FileProcessor class in the aggregator module.

3. **New Command-Line Option**: Add the option to the argument parser in the cli module and handle it appropriately.

4. **New Configuration Setting**: Add the setting to the default configuration in the config module.

5. **New TUI Feature**: Extend the FileSelector class in the tui module.

For more detailed information about each module, refer to their respective documentation pages.
