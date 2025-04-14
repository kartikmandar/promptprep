.. _api_aggregator:

Aggregator Module
================

The ``aggregator`` module is the core component of promptprep that handles file scanning, content extraction, and aggregation.

Module Overview
-------------

.. py:module:: promptprep.aggregator

The aggregator module provides functionality for:

- Scanning directories for code files
- Filtering files based on various criteria
- Extracting content from files
- Generating directory trees
- Processing files incrementally
- Generating diffs between versions

Key Classes and Functions
-----------------------

CodeAggregator
~~~~~~~~~~~~~

.. py:class:: CodeAggregator(directory='.', output_file='full_code.txt', include_files=None, exclude_dirs=None, extensions=None, max_file_size=100.0, include_comments=True, summary_mode=False, line_numbers=False, incremental=False, last_run_timestamp=None)

   The main class responsible for aggregating code files.

   :param str directory: The directory to scan for code files (default: current directory)
   :param str output_file: The file to save the output to (default: 'full_code.txt')
   :param list include_files: List of specific files to include (default: None)
   :param list exclude_dirs: List of directories to exclude (default: None)
   :param list extensions: List of file extensions to include (default: None)
   :param float max_file_size: Maximum file size in MB to include (default: 100.0)
   :param bool include_comments: Whether to include comments in the output (default: True)
   :param bool summary_mode: Whether to extract only signatures and docstrings (default: False)
   :param bool line_numbers: Whether to add line numbers to the output (default: False)
   :param bool incremental: Whether to process files incrementally (default: False)
   :param float last_run_timestamp: Timestamp of the last run for incremental processing (default: None)

   .. py:method:: scan_directory()

      Scan the directory for code files based on the configured filters.

      :return: A list of file paths that match the criteria
      :rtype: list

   .. py:method:: generate_directory_tree()

      Generate an ASCII representation of the directory structure.

      :return: ASCII directory tree
      :rtype: str

   .. py:method:: process_file(file_path)

      Process a single file and extract its content.

      :param str file_path: Path to the file to process
      :return: Processed content of the file
      :rtype: str

   .. py:method:: aggregate_code()

      Aggregate code from all matching files.

      :return: Aggregated code with directory tree and file headers
      :rtype: str

   .. py:method:: save_output(content)

      Save the aggregated content to the output file.

      :param str content: The content to save
      :return: None

   .. py:method:: generate_metadata()

      Generate metadata about the processed files.

      :return: Metadata as a formatted string
      :rtype: str

   .. py:method:: count_tokens(content, model='cl100k_base')

      Count the number of tokens in the content.

      :param str content: The content to count tokens in
      :param str model: The tokenizer model to use (default: 'cl100k_base')
      :return: Number of tokens
      :rtype: int

   .. py:method:: generate_diff(prev_file, context_lines=3)

      Generate a diff between the current output and a previous output file.

      :param str prev_file: Path to the previous output file
      :param int context_lines: Number of context lines to include in the diff (default: 3)
      :return: Diff as a formatted string
      :rtype: str

FileProcessor
~~~~~~~~~~~~

.. py:class:: FileProcessor(include_comments=True, summary_mode=False, line_numbers=False)

   Class responsible for processing individual files.

   :param bool include_comments: Whether to include comments in the output (default: True)
   :param bool summary_mode: Whether to extract only signatures and docstrings (default: False)
   :param bool line_numbers: Whether to add line numbers to the output (default: False)

   .. py:method:: process_file(file_path)

      Process a file and extract its content based on the configured options.

      :param str file_path: Path to the file to process
      :return: Processed content of the file
      :rtype: str

   .. py:method:: extract_summary(content, file_ext)

      Extract function/class signatures and docstrings from the content.

      :param str content: The file content
      :param str file_ext: The file extension
      :return: Extracted summary
      :rtype: str

   .. py:method:: add_line_numbers(content)

      Add line numbers to the content.

      :param str content: The content to add line numbers to
      :return: Content with line numbers
      :rtype: str

DirectoryTreeGenerator
~~~~~~~~~~~~~~~~~~~~

.. py:class:: DirectoryTreeGenerator(root_dir, exclude_dirs=None, include_files=None)

   Class responsible for generating ASCII directory trees.

   :param str root_dir: The root directory to generate the tree for
   :param list exclude_dirs: List of directories to exclude (default: None)
   :param list include_files: List of specific files to include (default: None)

   .. py:method:: generate_tree()

      Generate an ASCII representation of the directory structure.

      :return: ASCII directory tree
      :rtype: str

IncrementalProcessor
~~~~~~~~~~~~~~~~~~

.. py:class:: IncrementalProcessor(last_run_timestamp=None)

   Class responsible for incremental processing.

   :param float last_run_timestamp: Timestamp of the last run (default: None)

   .. py:method:: should_process_file(file_path, prev_output_file=None)

      Determine if a file should be processed based on its modification time.

      :param str file_path: Path to the file to check
      :param str prev_output_file: Path to the previous output file (default: None)
      :return: Whether the file should be processed
      :rtype: bool

   .. py:method:: extract_timestamp_from_file(file_path)

      Extract the timestamp from a previous output file.

      :param str file_path: Path to the file to extract the timestamp from
      :return: Extracted timestamp or None if not found
      :rtype: float or None

DiffGenerator
~~~~~~~~~~~

.. py:class:: DiffGenerator(context_lines=3)

   Class responsible for generating diffs between versions.

   :param int context_lines: Number of context lines to include in the diff (default: 3)

   .. py:method:: generate_diff(current_content, prev_file)

      Generate a diff between the current content and a previous output file.

      :param str current_content: The current content
      :param str prev_file: Path to the previous output file
      :return: Diff as a formatted string
      :rtype: str

Usage Examples
------------

Basic Usage
~~~~~~~~~~

.. code-block:: python

   from promptprep.aggregator import CodeAggregator

   # Create an aggregator
   aggregator = CodeAggregator(
       directory='./my_project',
       output_file='output.txt',
       exclude_dirs=['venv', 'node_modules'],
       extensions=['.py', '.js']
   )

   # Aggregate code
   content = aggregator.aggregate_code()

   # Save output
   aggregator.save_output(content)

With Metadata
~~~~~~~~~~~

.. code-block:: python

   from promptprep.aggregator import CodeAggregator

   aggregator = CodeAggregator(directory='./my_project')
   
   # Generate metadata
   metadata = aggregator.generate_metadata()
   
   # Aggregate code
   content = aggregator.aggregate_code()
   
   # Combine metadata and content
   full_content = metadata + '\n\n' + content
   
   # Save output
   aggregator.save_output(full_content)

Incremental Processing
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from promptprep.aggregator import CodeAggregator
   import time

   # First run
   aggregator = CodeAggregator(
       directory='./my_project',
       output_file='baseline.txt'
   )
   content = aggregator.aggregate_code()
   aggregator.save_output(content)

   # Later, after making changes
   timestamp = time.time()
   incremental_aggregator = CodeAggregator(
       directory='./my_project',
       output_file='updated.txt',
       incremental=True,
       last_run_timestamp=timestamp
   )
   updated_content = incremental_aggregator.aggregate_code()
   incremental_aggregator.save_output(updated_content)

Generating Diffs
~~~~~~~~~~~~~~

.. code-block:: python

   from promptprep.aggregator import CodeAggregator

   aggregator = CodeAggregator(
       directory='./my_project',
       output_file='current.txt'
   )
   content = aggregator.aggregate_code()
   
   # Generate diff with a previous version
   diff = aggregator.generate_diff('previous.txt', context_lines=5)
   
   # Save diff to a file
   with open('diff.txt', 'w') as f:
       f.write(diff)