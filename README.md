# PromptPrep

## Overview

**PromptPrep** aggregates all your programming-related code files from a specified directory into a single file with an ASCII directory tree. This is particularly useful when you want to provide your complete codebase to AI models or perform other analyses.

## Features

- **Directory Tree Generation**: Creates an ASCII representation of your directory structure (with configurable exclusions).
- **Code Aggregation**: Concatenates code from programming-related files into one master file.
- **Customizable Inclusions/Exclusions**: Specify which files or directories to include or omit using glob patterns.
- **Hidden File Handling**: Option to include hidden files and directories.
- **Summary Mode**: Option to include only function/class declarations and docstrings (for Python files).
- **Comment Filtering**: Option to exclude comments from the aggregated output.
- **Metadata Collection**: Option to gather and append basic codebase statistics (LOC, comment ratio, etc.).
- **CLI and API**: Use it directly from the command line or import classes/functions into your notebooks.

## Installation

You can install PromptPrep via pip:

```bash
pip install .
# Or for development:
pip install -e .
```

## Usage

```bash
promptprep <root_directory> <output_file> [options]
```

**Arguments:**

*   `root_directory`: The path to the directory you want to process.
*   `output_file`: The path where the aggregated output file will be saved.

**Options:**

*   `-i, --include <pattern>`: Glob pattern for files to include. Can be used multiple times. (Default: Includes common code file extensions)
*   `-e, --exclude <pattern>`: Glob pattern for files/directories to exclude. Can be used multiple times. (Default: Excludes common virtual environments, build artifacts, etc.)
*   `--hidden`: Include hidden files and directories (those starting with `.`).
*   `--summary`: Enable summary mode. Only include function/class declarations and docstrings from Python files. Other file types will be included as is.
*   `--no-comments`: Exclude comments from the aggregated output. Docstrings in Python files are generally preserved unless `--summary` mode is also active.
*   `--metadata`: Collect and append metadata (total files, lines of code, comment lines, blank lines, comment ratio) to the end of the output file.

**Example:**

```bash
promptprep ./my_project aggregated_code.txt -e "*/__pycache__/*" -e "*.tmp" --summary --metadata
```

This command will:

1.  Process the `./my_project` directory.
2.  Save the output to `aggregated_code.txt`.
3.  Exclude any files within `__pycache__` directories and any files ending with `.tmp`.
4.  Enable summary mode (declarations/docstrings only for Python).
5.  Append metadata statistics to the output file.

## Development

Clone the repository and install in editable mode:

```bash
git clone <repository_url>
cd PromptPrep
pip install -e .
```

Run tests using pytest:

```bash
pytest
```
