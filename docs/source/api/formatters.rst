.. _api_formatters:

Formatters Module
================

The ``formatters`` module provides different output formats for the aggregated code.

Module Overview
-------------

.. py:module:: promptprep.formatters

The formatters module provides functionality for:

- Formatting aggregated code in different output formats
- Applying syntax highlighting
- Handling custom templates
- Detecting the appropriate format based on file extension

Key Classes and Functions
-----------------------

FormatterFactory
~~~~~~~~~~~~~~

.. py:class:: FormatterFactory

   Factory class for creating the appropriate formatter based on the format name.

   .. py:classmethod:: create_formatter(format_name, template_file=None)

      Create a formatter instance based on the format name.

      :param str format_name: The name of the format ('plain', 'markdown', 'html', 'highlighted', or 'custom')
      :param str template_file: Path to the template file for custom format (default: None)
      :return: A formatter instance
      :rtype: BaseFormatter
      :raises ValueError: If the format name is not recognized

   .. py:classmethod:: detect_format_from_file(file_path)

      Detect the appropriate format based on the file extension.

      :param str file_path: Path to the output file
      :return: The detected format name
      :rtype: str

BaseFormatter
~~~~~~~~~~~

.. py:class:: BaseFormatter

   Base class for all formatters.

   .. py:method:: format_output(title, directory_tree, files_content, metadata=None, skipped_files=None)

      Format the aggregated code.

      :param str title: The title of the output
      :param str directory_tree: ASCII directory tree
      :param dict files_content: Dictionary mapping file paths to their content
      :param str metadata: Metadata about the codebase (default: None)
      :param list skipped_files: List of files that were skipped (default: None)
      :return: Formatted output
      :rtype: str

   .. py:method:: format_file_header(file_path)

      Format a file header.

      :param str file_path: Path to the file
      :return: Formatted file header
      :rtype: str

   .. py:method:: format_file_content(file_path, content)

      Format the content of a file.

      :param str file_path: Path to the file
      :param str content: Content of the file
      :return: Formatted file content
      :rtype: str

PlainFormatter
~~~~~~~~~~~~

.. py:class:: PlainFormatter

   Formatter for plain text output.

   .. py:method:: format_output(title, directory_tree, files_content, metadata=None, skipped_files=None)

      Format the aggregated code as plain text.

      :param str title: The title of the output
      :param str directory_tree: ASCII directory tree
      :param dict files_content: Dictionary mapping file paths to their content
      :param str metadata: Metadata about the codebase (default: None)
      :param list skipped_files: List of files that were skipped (default: None)
      :return: Formatted output as plain text
      :rtype: str

   .. py:method:: format_file_header(file_path)

      Format a file header as plain text.

      :param str file_path: Path to the file
      :return: Formatted file header
      :rtype: str

   .. py:method:: format_file_content(file_path, content)

      Format the content of a file as plain text.

      :param str file_path: Path to the file
      :param str content: Content of the file
      :return: Formatted file content
      :rtype: str

MarkdownFormatter
~~~~~~~~~~~~~~

.. py:class:: MarkdownFormatter

   Formatter for Markdown output.

   .. py:method:: format_output(title, directory_tree, files_content, metadata=None, skipped_files=None)

      Format the aggregated code as Markdown.

      :param str title: The title of the output
      :param str directory_tree: ASCII directory tree
      :param dict files_content: Dictionary mapping file paths to their content
      :param str metadata: Metadata about the codebase (default: None)
      :param list skipped_files: List of files that were skipped (default: None)
      :return: Formatted output as Markdown
      :rtype: str

   .. py:method:: format_file_header(file_path)

      Format a file header as Markdown.

      :param str file_path: Path to the file
      :return: Formatted file header
      :rtype: str

   .. py:method:: format_file_content(file_path, content)

      Format the content of a file as Markdown with syntax highlighting.

      :param str file_path: Path to the file
      :param str content: Content of the file
      :return: Formatted file content with Markdown code blocks
      :rtype: str

   .. py:method:: get_language_from_extension(file_path)

      Determine the language for syntax highlighting based on the file extension.

      :param str file_path: Path to the file
      :return: Language name for syntax highlighting
      :rtype: str

HTMLFormatter
~~~~~~~~~~~

.. py:class:: HTMLFormatter

   Formatter for HTML output.

   .. py:method:: format_output(title, directory_tree, files_content, metadata=None, skipped_files=None)

      Format the aggregated code as HTML.

      :param str title: The title of the output
      :param str directory_tree: ASCII directory tree
      :param dict files_content: Dictionary mapping file paths to their content
      :param str metadata: Metadata about the codebase (default: None)
      :param list skipped_files: List of files that were skipped (default: None)
      :return: Formatted output as HTML
      :rtype: str

   .. py:method:: format_file_header(file_path)

      Format a file header as HTML.

      :param str file_path: Path to the file
      :return: Formatted file header
      :rtype: str

   .. py:method:: format_file_content(file_path, content)

      Format the content of a file as HTML.

      :param str file_path: Path to the file
      :param str content: Content of the file
      :return: Formatted file content with HTML pre tags
      :rtype: str

HighlightedFormatter
~~~~~~~~~~~~~~~~~

.. py:class:: HighlightedFormatter

   Formatter for syntax-highlighted HTML output.

   .. py:method:: format_output(title, directory_tree, files_content, metadata=None, skipped_files=None)

      Format the aggregated code as syntax-highlighted HTML.

      :param str title: The title of the output
      :param str directory_tree: ASCII directory tree
      :param dict files_content: Dictionary mapping file paths to their content
      :param str metadata: Metadata about the codebase (default: None)
      :param list skipped_files: List of files that were skipped (default: None)
      :return: Formatted output as syntax-highlighted HTML
      :rtype: str

   .. py:method:: format_file_header(file_path)

      Format a file header as HTML.

      :param str file_path: Path to the file
      :return: Formatted file header
      :rtype: str

   .. py:method:: format_file_content(file_path, content)

      Format the content of a file with syntax highlighting.

      :param str file_path: Path to the file
      :param str content: Content of the file
      :return: Syntax-highlighted file content
      :rtype: str

   .. py:method:: highlight_code(code, lexer_name)

      Apply syntax highlighting to code.

      :param str code: Code to highlight
      :param str lexer_name: Name of the lexer to use for highlighting
      :return: Highlighted code as HTML
      :rtype: str

CustomFormatter
~~~~~~~~~~~~

.. py:class:: CustomFormatter(template_file)

   Formatter for custom output based on a template file.

   :param str template_file: Path to the template file

   .. py:method:: format_output(title, directory_tree, files_content, metadata=None, skipped_files=None)

      Format the aggregated code using a custom template.

      :param str title: The title of the output
      :param str directory_tree: ASCII directory tree
      :param dict files_content: Dictionary mapping file paths to their content
      :param str metadata: Metadata about the codebase (default: None)
      :param list skipped_files: List of files that were skipped (default: None)
      :return: Formatted output based on the template
      :rtype: str

   .. py:method:: load_template()

      Load the template from the template file.

      :return: Template content
      :rtype: str
      :raises FileNotFoundError: If the template file doesn't exist

   .. py:method:: replace_placeholders(template, title, directory_tree, files_content, metadata, skipped_files)

      Replace placeholders in the template with actual content.

      :param str template: Template content
      :param str title: The title of the output
      :param str directory_tree: ASCII directory tree
      :param dict files_content: Dictionary mapping file paths to their content
      :param str metadata: Metadata about the codebase
      :param list skipped_files: List of files that were skipped
      :return: Template with placeholders replaced
      :rtype: str

Usage Examples
------------

Basic Usage
~~~~~~~~~~

.. code-block:: python

   from promptprep.formatters import FormatterFactory

   # Create a formatter
   formatter = FormatterFactory.create_formatter('markdown')

   # Format output
   formatted_output = formatter.format_output(
       title="My Project",
       directory_tree="project/\n├── src/\n│   └── main.py\n└── README.md",
       files_content={
           "src/main.py": "def main():\n    print('Hello, world!')",
           "README.md": "# My Project\n\nA simple project."
       }
   )

   # Save to file
   with open('output.md', 'w') as f:
       f.write(formatted_output)

With Metadata
~~~~~~~~~~~

.. code-block:: python

   from promptprep.formatters import FormatterFactory

   formatter = FormatterFactory.create_formatter('html')
   
   formatted_output = formatter.format_output(
       title="My Project",
       directory_tree="project/\n├── src/\n│   └── main.py\n└── README.md",
       files_content={
           "src/main.py": "def main():\n    print('Hello, world!')",
           "README.md": "# My Project\n\nA simple project."
       },
       metadata="Files: 2\nLines: 5\nComments: 0",
       skipped_files=["large_file.bin"]
   )

Custom Template
~~~~~~~~~~~~~

.. code-block:: python

   from promptprep.formatters import FormatterFactory

   # Create a custom formatter with a template file
   formatter = FormatterFactory.create_formatter('custom', template_file='my_template.txt')
   
   formatted_output = formatter.format_output(
       title="My Project",
       directory_tree="project/\n├── src/\n│   └── main.py\n└── README.md",
       files_content={
           "src/main.py": "def main():\n    print('Hello, world!')",
           "README.md": "# My Project\n\nA simple project."
       }
   )

Format Detection
~~~~~~~~~~~~~~

.. code-block:: python

   from promptprep.formatters import FormatterFactory

   # Detect format from file extension
   output_file = 'output.md'
   format_name = FormatterFactory.detect_format_from_file(output_file)
   
   # Create formatter based on detected format
   formatter = FormatterFactory.create_formatter(format_name)
   
   # Format output
   formatted_output = formatter.format_output(
       title="My Project",
       directory_tree="project/\n├── src/\n│   └── main.py\n└── README.md",
       files_content={
           "src/main.py": "def main():\n    print('Hello, world!')",
           "README.md": "# My Project\n\nA simple project."
       }
   )