.. _api_config:

Config Module
============

The ``config`` module provides functionality for managing configuration settings in promptprep.

Module Overview
-------------

.. py:module:: promptprep.config

The config module provides functionality for:

- Loading configuration from files
- Saving configuration to files
- Managing default configuration settings
- Converting between different configuration formats

Key Functions
-----------

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

.. py:function:: save_config(config, config_file=None)

   Save configuration to a file.
   
   :param dict config: Configuration dictionary to save
   :param str config_file: Path to the configuration file (default: None, which uses the default location)
   :return: None

get_default_config_path
~~~~~~~~~~~~~~~~~~~~~

.. py:function:: get_default_config_path()

   Get the default path for the configuration file.
   
   :return: Default configuration file path
   :rtype: str

get_default_config
~~~~~~~~~~~~~~~~

.. py:function:: get_default_config()

   Get the default configuration settings.
   
   :return: Default configuration as a dictionary
   :rtype: dict

merge_configs
~~~~~~~~~~~

.. py:function:: merge_configs(base_config, override_config)

   Merge two configuration dictionaries, with override_config taking precedence.
   
   :param dict base_config: Base configuration dictionary
   :param dict override_config: Configuration dictionary to override base settings
   :return: Merged configuration dictionary
   :rtype: dict

validate_config
~~~~~~~~~~~~~

.. py:function:: validate_config(config)

   Validate a configuration dictionary.
   
   :param dict config: Configuration dictionary to validate
   :return: Validated configuration dictionary
   :rtype: dict
   :raises ValueError: If the configuration is invalid

normalize_config
~~~~~~~~~~~~~~

.. py:function:: normalize_config(config)

   Normalize a configuration dictionary (convert types, handle special cases).
   
   :param dict config: Configuration dictionary to normalize
   :return: Normalized configuration dictionary
   :rtype: dict

config_to_args
~~~~~~~~~~~~

.. py:function:: config_to_args(config)

   Convert a configuration dictionary to command-line arguments.
   
   :param dict config: Configuration dictionary
   :return: List of command-line arguments
   :rtype: list

args_to_config
~~~~~~~~~~~~

.. py:function:: args_to_config(args)

   Convert command-line arguments to a configuration dictionary.
   
   :param argparse.Namespace args: Command-line arguments
   :return: Configuration dictionary
   :rtype: dict

Configuration File Format
-----------------------

The configuration file is a JSON file with the following structure:

.. code-block:: json

   {
     "directory": "./my_project",
     "output_file": "output.md",
     "format": "markdown",
     "exclude_dirs": ["node_modules", "venv", "__pycache__"],
     "extensions": [".py", ".js", ".md"],
     "include_comments": true,
     "metadata": true,
     "count_tokens": true,
     "token_model": "cl100k_base",
     "line_numbers": false,
     "summary_mode": false,
     "max_file_size": 100.0
   }

All fields are optional and will use default values if not specified.

Default Configuration Location
----------------------------

The default location for the configuration file is:

- On Windows: ``C:\\Users\\<username>\\.promptprep\\config.json``
- On macOS/Linux: ``/home/<username>/.promptprep/config.json``

Usage Examples
------------

Basic Usage
~~~~~~~~~~

.. code-block:: python

   from promptprep.config import load_config, save_config

   # Load configuration
   config = load_config()
   
   # Modify configuration
   config['format'] = 'markdown'
   config['exclude_dirs'] = ['node_modules', 'venv']
   
   # Save configuration
   save_config(config)

Custom Configuration File
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from promptprep.config import load_config, save_config

   # Load from custom file
   config = load_config('my_config.json')
   
   # Save to custom file
   save_config(config, 'new_config.json')

Default Configuration
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from promptprep.config import get_default_config, get_default_config_path

   # Get default configuration
   default_config = get_default_config()
   print(f"Default configuration: {default_config}")
   
   # Get default configuration path
   config_path = get_default_config_path()
   print(f"Default configuration path: {config_path}")

Merging Configurations
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from promptprep.config import get_default_config, merge_configs

   # Get default configuration
   default_config = get_default_config()
   
   # Create custom overrides
   custom_config = {
       'format': 'markdown',
       'exclude_dirs': ['node_modules', 'venv']
   }
   
   # Merge configurations
   merged_config = merge_configs(default_config, custom_config)
   print(f"Merged configuration: {merged_config}")

Converting Between Formats
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from promptprep.config import args_to_config, config_to_args
   import argparse

   # Create argument parser
   parser = argparse.ArgumentParser()
   parser.add_argument('--format', default='plain')
   parser.add_argument('--directory', '-d', default='.')
   
   # Parse arguments
   args = parser.parse_args(['--format', 'markdown', '-d', './my_project'])
   
   # Convert arguments to configuration
   config = args_to_config(args)
   print(f"Configuration from args: {config}")
   
   # Convert configuration to arguments
   arg_list = config_to_args(config)
   print(f"Arguments from config: {arg_list}")

Validating Configuration
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from promptprep.config import validate_config, normalize_config

   # Create a configuration
   config = {
       'format': 'markdown',
       'exclude_dirs': 'node_modules,venv',  # String instead of list
       'max_file_size': '10'  # String instead of float
   }
   
   # Normalize configuration
   normalized_config = normalize_config(config)
   print(f"Normalized configuration: {normalized_config}")
   
   # Validate configuration
   try:
       validated_config = validate_config(normalized_config)
       print(f"Validated configuration: {validated_config}")
   except ValueError as e:
       print(f"Invalid configuration: {e}")

Creating a New Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from promptprep.config import get_default_config, save_config

   # Start with default configuration
   config = get_default_config()
   
   # Customize for a specific project
   config.update({
       'directory': './my_project',
       'format': 'markdown',
       'exclude_dirs': ['node_modules', 'venv', '__pycache__'],
       'extensions': ['.py', '.js', '.md'],
       'metadata': True,
       'count_tokens': True
   })
   
   # Save as a project-specific configuration
   save_config(config, 'my_project_config.json')