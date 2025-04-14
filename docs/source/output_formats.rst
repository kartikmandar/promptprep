.. _output_formats:

Output Formats
=============

promptprep supports multiple output formats to suit different needs. This page explains the available formats and how to use them.

Overview
--------

You can specify the output format using the ``--format`` option:

.. code-block:: bash

   promptprep --format FORMAT [other options]

Where ``FORMAT`` is one of the available formats described below.

Available Formats
----------------

Plain Text (Default)
~~~~~~~~~~~~~~~~~~~

The default format is plain text, which is simple and works everywhere:

.. code-block:: bash

   promptprep --format plain -o output.txt
   # or simply
   promptprep -o output.txt

Example output:

.. code-block:: text

   # Code Aggregation - my_project
   
   ## Directory Structure
   
   project/
   ├── src/
   │   ├── main.py
   │   └── utils.py
   └── tests/
       └── test_main.py
   
   ## File: src/main.py
   
   def main():
       print("Hello, world!")
       
   if __name__ == "__main__":
       main()
   
   ## File: src/utils.py
   
   def helper_function():
       return "I'm helping!"

Markdown
~~~~~~~

The Markdown format creates GitHub-friendly output with proper code blocks and syntax highlighting:

.. code-block:: bash

   promptprep --format markdown -o output.md

Example output:

.. code-block:: markdown

   # Code Aggregation - my_project
   
   ## Directory Structure
   
   ```
   project/
   ├── src/
   │   ├── main.py
   │   └── utils.py
   └── tests/
       └── test_main.py
   ```
   
   ## File: src/main.py
   
   ```python
   def main():
       print("Hello, world!")
       
   if __name__ == "__main__":
       main()
   ```
   
   ## File: src/utils.py
   
   ```python
   def helper_function():
       return "I'm helping!"
   ```

HTML
~~~~

The HTML format generates a complete webpage with basic styling:

.. code-block:: bash

   promptprep --format html -o output.html

This creates a self-contained HTML file with CSS styling that can be opened in any web browser.

Highlighted
~~~~~~~~~~

The highlighted format adds full syntax highlighting with colors to make your code more readable:

.. code-block:: bash

   promptprep --format highlighted -o output.html

This requires the optional ``pygments`` package:

.. code-block:: bash

   pip install promptprep[highlighting]

The result is an HTML file with syntax highlighting based on the file type.

Custom
~~~~~

The custom format lets you design your own output format using a template file:

.. code-block:: bash

   promptprep --format custom --template-file my_template.txt -o output.txt

See :ref:`custom_templates` for details on creating and using custom templates.

Format-Specific Features
----------------------

Line Numbers
~~~~~~~~~~~

You can add line numbers to the code in the output with the ``--line-numbers`` option:

.. code-block:: bash

   promptprep --format markdown --line-numbers -o output_with_lines.md

Example output with line numbers:

.. code-block:: markdown

   ## File: src/main.py
   
   ```python
   1  def main():
   2      print("Hello, world!")
   3      
   4  if __name__ == "__main__":
   5      main()
   ```

This works with all formats except custom (where you need to handle line numbers in your template).

Format Detection from Output File
-------------------------------

promptprep can automatically detect the desired format based on the output file extension:

.. code-block:: bash

   promptprep -o output.md  # Uses markdown format
   promptprep -o output.html  # Uses html format

The mapping is:
- ``.md``: markdown
- ``.html``: html
- ``.htm``: html
- Other extensions: plain

You can override this by explicitly specifying the format:

.. code-block:: bash

   promptprep --format markdown -o output.txt  # Uses markdown format despite .txt extension

Choosing the Right Format
-----------------------

Each format has its strengths and is suited for different use cases:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Format
     - Strengths
     - Best For
   * - **plain**
     - Simple, works everywhere, no dependencies
     - Quick snapshots, universal compatibility
   * - **markdown**
     - Good readability, works on GitHub, syntax highlighting
     - Sharing on GitHub, documentation, AI model prompts
   * - **html**
     - Interactive, can be opened in browsers
     - Sharing with non-technical users, documentation
   * - **highlighted**
     - Best readability, full syntax highlighting
     - Code reviews, presentations, documentation
   * - **custom**
     - Complete flexibility
     - Specialized outputs, integration with other tools

Best Practices
-------------

1. **Match Format to Audience**: Choose a format that works best for your intended audience.

2. **Consider File Size**: HTML and highlighted formats may produce larger files.

3. **Use Markdown for AI Models**: When sharing with AI models like GPT-4, the markdown format works best.

4. **Add Line Numbers for Reference**: Use ``--line-numbers`` when you need to reference specific lines.

5. **Combine with Metadata**: Add ``--metadata`` to include useful statistics about your codebase.

Examples
-------

For AI Model Assistance
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep -d ./my_project --format markdown --metadata --count-tokens -c

This creates markdown output with metadata and token count, and copies it to your clipboard for pasting into an AI chat.

For Documentation
~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep -d ./src --format highlighted -o documentation.html

This creates a syntax-highlighted HTML file that can be shared as documentation.

For Code Reviews
~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep -d ./feature_branch --diff main_branch.txt --format highlighted --line-numbers -o review.html

This creates a syntax-highlighted HTML file with line numbers showing what changed between branches.

For Quick Reference
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   promptprep -d . --summary-mode --format plain -o quick_reference.txt

This creates a plain text file with only function/class signatures and docstrings for quick reference.

Troubleshooting
--------------

If you encounter issues with output formats:

1. **Missing Dependencies**: For highlighted format, ensure you have installed the highlighting extra.

2. **Format Not Recognized**: Check that you're using one of the supported format names.

3. **Custom Template Issues**: Verify that your custom template file exists and contains valid placeholders.

4. **Line Numbers Not Showing**: Ensure you're using the ``--line-numbers`` option with a compatible format.