.. _incremental_processing:

Incremental Processing
=====================

Incremental processing is a powerful feature that allows promptprep to only process files that have changed since the last run. This can significantly improve performance when working with large codebases.

Overview
--------

When you run promptprep with the ``--incremental`` option, it will:

1. Check the modification time of each file
2. Compare it with the last run timestamp
3. Only process files that have been modified since the last run
4. Include unchanged files from the previous output

This approach saves time and resources, especially for large projects where only a few files change between runs.

Basic Usage
----------

To use incremental processing:

.. code-block:: bash

   promptprep --incremental [other options]

When you use the ``--incremental`` option without specifying a timestamp, promptprep will:

1. Look for a previous output file (specified with ``-o, --output-file``)
2. Extract the timestamp from that file
3. Use that timestamp as the reference point

If no previous output file exists or the timestamp can't be extracted, promptprep will process all files.

Specifying a Timestamp
---------------------

You can explicitly specify the reference timestamp using the ``--last-run-timestamp`` option:

.. code-block:: bash

   promptprep --incremental --last-run-timestamp 1678886400.0 [other options]

The timestamp should be a Unix timestamp (seconds since January 1, 1970). You can generate a timestamp in various ways:

- In Python: ``import time; print(time.time())``
- In Bash: ``date +%s``
- In JavaScript: ``Math.floor(Date.now() / 1000)``

Example Workflow
--------------

Here's a typical workflow using incremental processing:

1. Initial run:

   .. code-block:: bash

      promptprep -d ./my_project -o snapshot.txt

2. Later, after making changes to some files:

   .. code-block:: bash

      promptprep -d ./my_project --incremental -o updated_snapshot.txt

3. promptprep will:
   - Detect which files have changed since the creation of ``snapshot.txt``
   - Only process those changed files
   - Include unchanged files from ``snapshot.txt``
   - Save the result to ``updated_snapshot.txt``

Combining with Other Features
---------------------------

Incremental processing works well with other promptprep features:

With Diff Generation
~~~~~~~~~~~~~~~~~~~

Track changes over time by combining incremental processing with diff generation:

.. code-block:: bash

   # First run
   promptprep -d . -o baseline.txt

   # Later, after making changes
   promptprep -d . --incremental --diff baseline.txt -o changes.txt

This will show you exactly what changed between runs.

With Metadata
~~~~~~~~~~~~

Get statistics about your changes:

.. code-block:: bash

   promptprep -d . --incremental --metadata -o updated_snapshot.txt

The metadata will include information about how many files were processed incrementally.

With Different Output Formats
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Incremental processing works with all output formats:

.. code-block:: bash

   promptprep -d . --incremental --format markdown -o snapshot.md
   promptprep -d . --incremental --format html -o snapshot.html

Advanced Use Cases
----------------

Continuous Integration
~~~~~~~~~~~~~~~~~~~~

In a CI/CD pipeline, you can use incremental processing to only analyze files that have changed in a pull request:

.. code-block:: bash

   # Get the base branch timestamp
   BASE_TIMESTAMP=$(git show --format=%at -s origin/main)

   # Process only files that changed since the base branch
   promptprep -d . --incremental --last-run-timestamp $BASE_TIMESTAMP -o pr_changes.txt

Scheduled Snapshots
~~~~~~~~~~~~~~~~~

Create regular snapshots of your codebase, processing only what has changed:

.. code-block:: bash

   # In a cron job or scheduled task
   TIMESTAMP=$(date +%s)
   promptprep -d . --incremental -o "snapshots/snapshot_$TIMESTAMP.txt"

Performance Considerations
-------------------------

Incremental processing can significantly improve performance, but there are some factors to consider:

File Count vs. File Size
~~~~~~~~~~~~~~~~~~~~~~~

The performance benefit depends on:

- The number of files in your project
- The size of those files
- The percentage of files that have changed

For projects with many large files where only a few files change between runs, the performance improvement can be substantial.

Overhead
~~~~~~~

There is some overhead involved in:

- Reading the previous output file
- Extracting unchanged content
- Checking file modification times

For very small projects, this overhead might outweigh the benefits.

Best Practices
-------------

1. **Keep Previous Outputs**: Store previous output files if you plan to use incremental processing.

2. **Use with Version Control**: Incremental processing works well with version-controlled projects where changes are tracked.

3. **Consider File Patterns**: Use with ``-x, --extensions`` and ``-e, --exclude-dirs`` to focus on relevant files.

4. **Verify Results**: Occasionally run a full (non-incremental) process to ensure consistency.

Troubleshooting
--------------

If incremental processing isn't working as expected:

1. **Check Timestamps**: Ensure the timestamp is in the correct format (Unix timestamp).

2. **Verify File Modification Times**: Some file systems or operations might not update modification times correctly.

3. **Check Previous Output**: Make sure the previous output file exists and is readable.

4. **Run with Verbose Output**: Add the ``-v, --verbose`` flag to see more information about what promptprep is doing.

Limitations
----------

There are some limitations to be aware of:

1. **Deleted Files**: If files have been deleted since the last run, they might still appear in the output unless you use the ``--diff`` option.

2. **Renamed Files**: Renamed files are treated as new files, as promptprep tracks changes based on file paths.

3. **Configuration Changes**: If you change configuration options (like excluded directories), you should run a full process instead of an incremental one.