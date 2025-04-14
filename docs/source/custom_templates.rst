.. _custom_templates:

Custom Templates
===============

The custom template feature gives you complete control over the structure and appearance of your output. This page explains how to create and use custom templates with promptprep.

Overview
--------

Custom templates are text files with special placeholders that promptprep will replace with actual content. This allows you to design exactly how your output should look.

Using Custom Templates
---------------------

To use a custom template:

1. Create a template file with placeholders (see below)
2. Run promptprep with the custom format and template file:

   .. code-block:: bash

      promptprep --format custom --template-file my_template.txt -o output.txt

Available Placeholders
---------------------

You can use the following placeholders in your template file:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Placeholder
     - Description
   * - ``${TITLE}``
     - The project title (e.g., "Code Aggregation - MyProject")
   * - ``${DIRECTORY_TREE}``
     - ASCII directory structure visualization
   * - ``${METADATA}``
     - Statistics about your code (only if you use ``--metadata``)
   * - ``${SKIPPED_FILES}``
     - List of any files that were too large to include
   * - ``${FILES}``
     - All your code files with their headers
   * - ``${FILE_HEADER:path/to/file.py}``
     - Header for a specific file
   * - ``${FILE_CONTENT:path/to/file.py}``
     - Content of a specific file

Example Template
---------------

Here's a simple template to get you started:

.. code-block:: text

    # Project Aggregation: ${TITLE}

    ## Directory Structure
    ${DIRECTORY_TREE}

    ## Code Files

    ### Main Application File
    ${FILE_HEADER:src/app.py}
    ${FILE_CONTENT:src/app.py}

    ### Utility Functions
    ${FILE_HEADER:src/utils.py}
    ${FILE_CONTENT:src/utils.py}

    ## Project Statistics
    ${METADATA}

    ## Skipped Files (Too Large)
    ${SKIPPED_FILES}

    --- End of Report ---

Advanced Template Examples
-------------------------

Markdown Template
~~~~~~~~~~~~~~~~

Here's a template for creating a well-structured Markdown document:

.. code-block:: text

    # ${TITLE}

    *Generated on: [current date]*

    ## Project Overview

    This document contains code from the project directory structure shown below.

    ```
    ${DIRECTORY_TREE}
    ```

    ## Project Statistics

    ${METADATA}

    ## Code Files

    ${FILES}

    ## Appendix

    ### Skipped Files
    
    The following files were too large to include:
    
    ${SKIPPED_FILES}

HTML Template
~~~~~~~~~~~~

Here's a template for creating a custom HTML document:

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
        <title>${TITLE}</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
            pre { background-color: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }
            .file-header { background-color: #e0e0e0; padding: 5px 10px; margin-top: 20px; border-radius: 5px 5px 0 0; }
            .file-content { margin-top: 0; border-radius: 0 0 5px 5px; }
            .metadata { background-color: #f0f7fb; border-left: 5px solid #3498db; padding: 10px; }
        </style>
    </head>
    <body>
        <h1>${TITLE}</h1>
        
        <h2>Directory Structure</h2>
        <pre>${DIRECTORY_TREE}</pre>
        
        <h2>Project Statistics</h2>
        <div class="metadata">
            <pre>${METADATA}</pre>
        </div>
        
        <h2>Code Files</h2>
        
        <div class="file-header">src/app.py</div>
        <pre class="file-content">${FILE_CONTENT:src/app.py}</pre>
        
        <div class="file-header">src/utils.py</div>
        <pre class="file-content">${FILE_CONTENT:src/utils.py}</pre>
        
        <h2>Skipped Files</h2>
        <pre>${SKIPPED_FILES}</pre>
    </body>
    </html>

Selective File Template
~~~~~~~~~~~~~~~~~~~~~~

This template only includes specific files that you're interested in:

.. code-block:: text

    # Selected Files from ${TITLE}

    ## Project Structure
    ${DIRECTORY_TREE}

    ## Main Files

    ### Main Entry Point
    ${FILE_HEADER:src/main.py}
    ${FILE_CONTENT:src/main.py}

    ### Core Logic
    ${FILE_HEADER:src/core.py}
    ${FILE_CONTENT:src/core.py}

    ## Test Files

    ### Main Tests
    ${FILE_HEADER:tests/test_main.py}
    ${FILE_CONTENT:tests/test_main.py}

Best Practices
-------------

1. **Start Simple**: Begin with a basic template and gradually add more complexity.

2. **Test Incrementally**: Test your template with a small subset of files first.

3. **Use Specific File Placeholders**: For important files, use specific placeholders like `${FILE_CONTENT:path/to/file.py}` instead of relying on `${FILES}`.

4. **Include Fallbacks**: For specific file placeholders, consider what should happen if the file doesn't exist.

5. **Consider the Output Format**: Design your template with the final output format in mind (plain text, Markdown, HTML, etc.).

6. **Add Context**: Include metadata, timestamps, and other contextual information to make your output more useful.

Troubleshooting
--------------

If your template isn't working as expected:

1. **Check File Paths**: Ensure that file paths in placeholders match exactly with the files in your project.

2. **Verify Placeholder Syntax**: Make sure placeholders are written exactly as shown (e.g., `${TITLE}`, not `{TITLE}` or `$TITLE`).

3. **Run with Verbose Output**: Add the `-v` or `--verbose` flag to see more information about what promptprep is doing.

4. **Check for Missing Files**: If you're using specific file placeholders, make sure those files exist in your project.