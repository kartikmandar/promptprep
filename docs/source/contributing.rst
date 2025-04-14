.. _contributing:

Contributing
===========

Thank you for your interest in contributing to promptprep! This guide will help you get started with contributing to the project.

Getting Started
--------------

Prerequisites
~~~~~~~~~~~~

Before you begin, ensure you have the following:

* Python 3.10 or higher
* Git
* A GitHub account

Setting Up the Development Environment
------------------------------------

1. Fork the repository on GitHub:
   
   * Visit https://github.com/kartikmandar/promptprep
   * Click the "Fork" button in the top-right corner

2. Clone your fork locally:

   .. code-block:: bash

      git clone https://github.com/YOUR-USERNAME/promptprep.git
      cd promptprep

3. Set up a virtual environment:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

4. Install the package in development mode with all development dependencies:

   .. code-block:: bash

      pip install -e ".[dev]"

5. Set up the upstream remote:

   .. code-block:: bash

      git remote add upstream https://github.com/kartikmandar/promptprep.git

Development Workflow
------------------

1. Create a new branch for your feature or bugfix:

   .. code-block:: bash

      git checkout -b feature-name

2. Make your changes to the codebase.

3. Run the tests to ensure your changes don't break existing functionality:

   .. code-block:: bash

      pytest

4. Format your code with Black:

   .. code-block:: bash

      black .

5. Run the linter to check for code quality issues:

   .. code-block:: bash

      ruff check .

6. Commit your changes with a descriptive message:

   .. code-block:: bash

      git add .
      git commit -m "Add feature X" or "Fix bug Y"

7. Push your changes to your fork:

   .. code-block:: bash

      git push origin feature-name

8. Create a pull request on GitHub:
   
   * Visit your fork at https://github.com/YOUR-USERNAME/promptprep
   * Click "Compare & pull request"
   * Fill out the pull request template with details about your changes

Code Style Guidelines
-------------------

We follow these coding standards:

* **PEP 8**: The Python style guide, with some modifications as defined in our Black configuration.
* **Black**: We use Black for code formatting with a line length of 88 characters.
* **Docstrings**: We use Google-style docstrings for all public functions, classes, and methods.

Example of a well-formatted function with docstring:

.. code-block:: python

   def process_file(file_path, include_comments=True, summary_mode=False):
       """Process a single file and return its content.
       
       Args:
           file_path (str): Path to the file to process.
           include_comments (bool, optional): Whether to include comments. Defaults to True.
           summary_mode (bool, optional): Whether to extract only signatures and docstrings. 
               Defaults to False.
               
       Returns:
           str: The processed content of the file.
           
       Raises:
           FileNotFoundError: If the file doesn't exist.
           PermissionError: If the file can't be read.
       """
       # Implementation here...

Testing Guidelines
----------------

We use pytest for testing. All new features should include tests, and all bug fixes should include tests that verify the fix.

1. **Test Location**: Tests should be placed in the `tests/` directory with a filename that matches the module being tested, prefixed with `test_`.

2. **Test Coverage**: We aim for high test coverage. Use `pytest-cov` to check coverage:

   .. code-block:: bash

      pytest --cov=promptprep

3. **Test Types**:
   
   * **Unit Tests**: Test individual functions and classes in isolation.
   * **Integration Tests**: Test how components work together.
   * **Functional Tests**: Test the CLI and end-to-end functionality.

Documentation Guidelines
----------------------

We use Sphinx for documentation. All new features should be documented.

1. **Docstrings**: All public functions, classes, and methods should have Google-style docstrings.

2. **RST Files**: Feature documentation should be added to the appropriate RST file in the `docs/source/` directory.

3. **Building Docs**: You can build the documentation locally to preview your changes:

   .. code-block:: bash

      cd docs
      make html
      # Open build/html/index.html in your browser

4. **README Updates**: If your changes affect the basic usage or installation, update the README.md file as well.

Pull Request Process
------------------

1. **Create a Focused PR**: Each pull request should address a single feature or bug fix.

2. **Write a Clear Description**: Explain what your changes do and why they're needed.

3. **Include Tests**: Ensure your changes are covered by tests.

4. **Update Documentation**: Add or update documentation for your changes.

5. **Pass CI Checks**: Make sure all CI checks pass before requesting a review.

6. **Address Review Feedback**: Be responsive to review feedback and make requested changes.

7. **Squash Commits**: Before merging, squash your commits into a single, well-described commit.

Release Process
-------------

The project maintainers follow these steps for releases:

1. Update the version number in `pyproject.toml` using `bump-my-version`.
2. Update the changelog with the new version and its changes.
3. Create a new release on GitHub with release notes.
4. Publish the new version to PyPI.

Getting Help
----------

If you need help with contributing:

* Open an issue on GitHub with your question
* Reach out to the maintainers directly

Thank you for contributing to promptprep!