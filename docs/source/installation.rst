.. _installation:

Installation
===========

This page provides detailed instructions for installing promptprep on different platforms.

Prerequisites
------------

Before installing promptprep, ensure you have the following:

* Python 3.10 or higher
* pip (Python package installer)

Installation Methods
-------------------

From PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to install promptprep is from PyPI using pip:

.. code-block:: bash

   pip install promptprep

This will install the latest stable version of promptprep and its required dependencies.

From Source
~~~~~~~~~~~

If you want the latest development version or plan to contribute to the project, you can install from source:

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/kartikmandar/promptprep.git
      cd promptprep

2. Install the package:

   .. code-block:: bash

      pip install .

   For development installation (changes to the code take effect immediately):

   .. code-block:: bash

      pip install -e .

Optional Dependencies
--------------------

promptprep has optional features that require additional dependencies:

Syntax Highlighting
~~~~~~~~~~~~~~~~~~

For syntax highlighting in the output, install with the highlighting extra:

.. code-block:: bash

   pip install promptprep[highlighting]

Or if installing from source:

.. code-block:: bash

   pip install .[highlighting]

Development Tools
~~~~~~~~~~~~~~~~

If you're contributing to promptprep, install the development dependencies:

.. code-block:: bash

   pip install promptprep[dev]

Or if installing from source:

.. code-block:: bash

   pip install .[dev]

Documentation Tools
~~~~~~~~~~~~~~~~~~

To build the documentation locally:

.. code-block:: bash

   pip install promptprep[docs]

Or if installing from source:

.. code-block:: bash

   pip install .[docs]

All Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

To install all optional dependencies:

.. code-block:: bash

   pip install promptprep[all]

Or if installing from source:

.. code-block:: bash

   pip install .[all]

Verifying Installation
---------------------

After installation, verify that promptprep is installed correctly by running:

.. code-block:: bash

   promptprep --version

This should display the version number of promptprep.

Upgrading
---------

To upgrade to the latest version:

.. code-block:: bash

   pip install --upgrade promptprep

Troubleshooting
--------------

If you encounter any issues during installation:

1. Ensure you have the latest version of pip:

   .. code-block:: bash

      pip install --upgrade pip

2. If you're using a virtual environment, make sure it's activated.

3. On some systems, you might need to use `pip3` instead of `pip`.

4. If you encounter permission errors, try using:

   .. code-block:: bash

      pip install --user promptprep

5. For any other issues, please check the :ref:`installation:troubleshooting` section or open an issue on the `GitHub repository <https://github.com/kartikmandar/promptprep/issues>`_.