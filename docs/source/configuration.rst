.. _configuration:

Configuration Management
=======================

promptprep allows you to save your favorite command options for quick reuse. This page explains how to manage configurations effectively.

Overview
--------

If you find yourself using the same set of options repeatedly, you can save them to a configuration file and load them later. This saves time and ensures consistency across multiple runs.

Saving Configuration
-------------------

To save your current options to a configuration file, use the ``--save-config`` flag:

.. code-block:: bash

   promptprep [options] --save-config [FILE]

If you don't specify a file path, promptprep will save to the default location (``~/.promptprep/config.json``).

Examples:

.. code-block:: bash

   # Save to default location
   promptprep -d ./my_project --summary-mode --metadata --save-config

   # Save to a custom file
   promptprep -d ./my_project --format markdown --save-config my_settings.json

Loading Configuration
--------------------

To load options from a configuration file, use the ``--load-config`` flag:

.. code-block:: bash

   promptprep --load-config [FILE] [additional options]

If you don't specify a file path, promptprep will load from the default location (``~/.promptprep/config.json``).

Examples:

.. code-block:: bash

   # Load from default location
   promptprep --load-config

   # Load from a custom file
   promptprep --load-config my_settings.json

   # Load from default location but override output file
   promptprep --load-config -o new_output.txt

Overriding Loaded Options
-------------------------

When you load a configuration file, you can override specific options by providing them on the command line:

.. code-block:: bash

   # Load settings but use a different output file and format
   promptprep --load-config my_settings.json -o different_output.md --format markdown

The command-line options take precedence over the options in the configuration file.

Default Location
---------------

promptprep stores configurations in ``~/.promptprep/config.json`` by default. This location is:

- On Windows: ``C:\\Users\\<username>\\.promptprep\\config.json``
- On macOS/Linux: ``/home/<username>/.promptprep/config.json``

Configuration File Format
------------------------

The configuration file is a JSON file that stores all the options you specified when saving. Here's an example:

.. code-block:: json

   {
     "directory": "./my_project",
     "output_file": "output.md",
     "format": "markdown",
     "exclude_dirs": ["node_modules", "venv", "__pycache__"],
     "extensions": [".py", ".js", ".md"],
     "include_comments": true,
     "metadata": true,
     "count_tokens": true
   }

You can manually edit this file if needed, but it's recommended to use the ``--save-config`` option to ensure the format is correct.

Managing Multiple Configurations
-------------------------------

You can create and manage multiple configuration files for different projects or use cases:

.. code-block:: bash

   # Save project-specific configurations
   promptprep -d ./project1 -x ".py,.js" --save-config project1_settings.json
   promptprep -d ./project2 -x ".ts,.jsx" --save-config project2_settings.json

   # Load project-specific configurations
   promptprep --load-config project1_settings.json
   promptprep --load-config project2_settings.json

This allows you to quickly switch between different sets of options for different projects.

Sharing Configurations
---------------------

You can share configuration files with team members to ensure everyone uses the same settings:

1. Save your configuration to a file:

   .. code-block:: bash

      promptprep [options] --save-config team_settings.json

2. Share the configuration file with your team members.

3. Team members can use the configuration:

   .. code-block:: bash

      promptprep --load-config team_settings.json

This ensures consistency across the team and reduces the chance of errors.

Best Practices
-------------

1. **Create Project-Specific Configurations**: Save different configurations for different projects or use cases.

2. **Include in Version Control**: Consider including your configuration files in version control to share with team members.

3. **Document Your Configurations**: Add comments or documentation explaining what each configuration is for.

4. **Review Before Using**: Always review the options in a configuration file before using it, especially if it was created by someone else.

5. **Update Regularly**: Update your configurations as your needs change or as new features are added to promptprep.

Troubleshooting
--------------

If you encounter issues with configuration files:

1. **Check File Permissions**: Ensure you have permission to read/write the configuration file.

2. **Verify JSON Format**: Make sure the configuration file is valid JSON. You can use online JSON validators to check.

3. **Check File Path**: Ensure you're specifying the correct path to the configuration file.

4. **Try Default Location**: If you're having trouble with a custom file, try using the default location instead.

5. **Reset to Default**: If all else fails, you can delete the configuration file and start fresh.