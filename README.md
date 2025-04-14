PromptPrep
==========

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

Table of Contents
-----------------

- [PromptPrep](#promptprep)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [From Source](#from-source)
  - [Usage](#usage)
    - [Basic Command](#basic-command)
    - [Common Options](#common-options)
    - [Example Commands](#example-commands)
  - [Command-Line Reference](#command-line-reference)
    - [Core Options](#core-options)
    - [File Selection \& Filtering](#file-selection--filtering)
    - [Content Processing](#content-processing)
    - [Output Formatting](#output-formatting)
    - [Incremental Processing](#incremental-processing)
    - [File Comparison (Diff)](#file-comparison-diff)
    - [Configuration Management](#configuration-management)
    - [Saving Configuration](#saving-configuration)
    - [Loading Configuration](#loading-configuration)
    - [Default Location](#default-location)
  - [Key Concepts Explained](#key-concepts-explained)
    - [File Aggregation](#file-aggregation)
    - [Directory Tree](#directory-tree)
    - [Interactive Mode (TUI)](#interactive-mode-tui)
    - [Summary Mode](#summary-mode)
    - [Incremental Processing](#incremental-processing-1)
    - [Diff Generation](#diff-generation)
    - [Metadata \& Token Counting](#metadata--token-counting)
  - [Output Formats](#output-formats)
    - [Available Formats](#available-formats)
    - [Selecting a Format](#selecting-a-format)
  - [Custom Templates](#custom-templates)
    - [Using Custom Templates](#using-custom-templates)
    - [Available Placeholders](#available-placeholders)
    - [Example Template](#example-template)
  - [Configuration Management](#configuration-management-1)
    - [Saving Configuration](#saving-configuration-1)
    - [Loading Configuration](#loading-configuration-1)
    - [Default Location](#default-location-1)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [License](#license)

Overview
--------

Hey there! **PromptPrep** is a handy command-line tool I built to help you bundle your code from multiple files into one neat, well-organized output file. It creates a visual map of your project structure and brings together all your selected files, making it perfect for:

* **Working with AI models:** Need to give GPT-4 or other LLMs context about your codebase for help with debugging or generating new code? PromptPrep packages everything they need to understand your project.

* **Creating documentation snapshots:** Capture your entire project's structure and code in one file for easy sharing or archiving.

* **Analyzing your project:** Get useful stats about your code (like line counts and comment ratios) to better understand your codebase.

* **Code reviews:** Share a consolidated view of specific parts of your project to make reviews more efficient.

The tool gives you full control over which files to include, how to process their content, and how you want the final output to look.

Features
--------

Here's what PromptPrep can do for you:

* **Bundle Your Code:** Combine multiple source files into one organized output file.
* **Visualize Project Structure:** See your directory structure in a clean ASCII tree format.
* **Smart File Selection:**
  * Cherry-pick specific files or exclude directories you don't need
  * Focus on just the file types that matter with extension filtering
  * Skip those massive files that would bloat your output
  * Automatically exclude common directories like `node_modules` and `__pycache__`
* **Interactive Selection:** Browse and pick files with a simple terminal interface - no more typing long paths!
* **Content Processing:**
  * **Summary Mode:** Just want the function/class signatures and docstrings? No problem!
  * **Comment Control:** Keep or strip comments from the output
  * **Line Numbers:** Add them when they help with readability and references
* **Multiple Output Formats:**
  * `plain`: Clean text output (default and simplest)
  * `markdown`: GitHub-friendly Markdown with code blocks
  * `html`: Complete webpage with basic styling
  * `highlighted`: Syntax-highlighted code (needs `pygments` package)
  * `custom`: Design your own output format with templates
* **Codebase Analytics:** Get stats about your files, lines of code, and comment ratios
* **Token Counting:** See how many tokens your code will use when sent to AI models like GPT-4
* **Incremental Processing:** Only process files that have changed since your last run
* **Diff Generation:** Compare versions to see what changed between runs
* **Save Your Settings:** Store your favorite command options for quick reuse
* **Clipboard Integration:** Send output directly to your clipboard, ready to paste

Installation
------------

### Prerequisites

You'll need:
* Python 3.7 or higher
* pip (the Python package installer)

### From Source

1. **Get the code:**
    ```bash
    git clone https://github.com/kartikmandar/PromptPrep
    cd promptprep
    ```

2. **Install it:**
    ```bash
    pip install .
    ```

3. **For developers:**
    If you want to tinker with the code, use the editable install:
    ```bash
    pip install -e .
    ```
    This way your changes take effect immediately without reinstalling.


Usage
-----

### Basic Command

It's super simple to get started:

```bash
promptprep [options]
```

If you run it without options, it'll process all code files in your current directory and save them to `full_code.txt`.

### Common Options

Here are the options you'll probably use most often:

* `-d, --directory DIR`: Which directory should I scan? (defaults to current)
* `-o, --output-file FILE`: Where should I save the output? (defaults to `full_code.txt`)
* `-c, --clipboard`: Send straight to clipboard instead of creating a file
* `-i, --include-files LIST`: Only include these specific files (comma-separated)
* `-e, --exclude-dirs LIST`: Skip these directories (comma-separated, like `node_modules,venv`)
* `-x, --extensions LIST`: Only include these file types (comma-separated, like `.py,.js`)
* `--format FORMAT`: Choose your output style (`plain`, `markdown`, `html`, `highlighted`, `custom`)
* `--interactive`: Launch the visual file picker in your terminal

### Example Commands

Here are some real-world examples to get you going:

1.  **Basic use - current folder to output.txt:**
    ```bash
    promptprep -o output.txt
    ```

2.  **Process a specific project:**
    ```bash
    promptprep -d ./my_project -o project_code.md --format markdown
    ```

3.  **Get a high-level overview with stats:**
    ```bash
    promptprep -d ./src --summary-mode --metadata --no-include-comments -o summary.txt
    ```

4.  **Just Python and JavaScript files, skip build folders:**
    ```bash
    promptprep -d . -x ".py,.js" -e "dist,.cache" -o web_code.txt
    ```

5.  **Pick files interactively and copy to clipboard:**
    ```bash
    promptprep -d ./my_app --interactive -c
    ```

6.  **Create a pretty HTML report with syntax highlighting:**
    ```bash
    promptprep -d . --format highlighted -o report.html
    ```

7.  **See what changed since last time:**
    ```bash
    # First run (or save previous state)
    promptprep -d . -o project_v1.txt
    # After making code changes...
    promptprep --diff project_v1.txt -o project_v2.txt
    ```

Command-Line Reference
----------------------

Here's the complete toolkit of options you can use with PromptPrep:

### Core Options

* `-d, --directory DIR`: Where should I look for code? (default: your current directory)
* `-o, --output-file FILE`: What should I name the output file? (default: `full_code.txt`)
* `-c, --clipboard`: Skip the file and copy directly to your clipboard instead

### File Selection & Filtering

* `-i, --include-files LIST`: Only process these specific files (comma-separated relative paths)
* `-e, --exclude-dirs LIST`: Skip these directories (like `venv,node_modules`) - overrides defaults
* `-x, --extensions LIST`: Only include these file types (like `.py,.js`) - overrides defaults
* `-m, --max-file-size MB`: Skip files larger than this size in MB (default: 100.0)
* `--interactive`: Launch the visual file picker to select what you want

### Content Processing

* `--summary-mode`: Just extract function/class signatures and docstrings - perfect for getting the big picture
* `--include-comments`: Keep comments in the output (this is the default)
* `--no-include-comments`: Strip out all comments (takes priority over `--include-comments`)
* `--metadata`: Add stats about your codebase at the beginning
* `--count-tokens`: Count how many tokens your code uses (needs `--metadata`)
* `--token-model MODEL`: Pick which tokenizer to use (default: `cl100k_base` for GPT-4)

### Output Formatting

* `--format FORMAT`: How should the output look? Options: `plain`, `markdown`, `html`, `highlighted`, or `custom`
* `--line-numbers`: Add line numbers to make referencing code easier
* `--template-file FILE`: Your custom template file (required if using `--format custom`)

### Incremental Processing

* `--incremental`: Only process files that have changed since last run
* `--last-run-timestamp TS`: When was the last run? (Unix timestamp, like `1678886400.0`)

### File Comparison (Diff)

* `--diff PREV_FILE`: Compare with a previous output file and show what changed
* `--diff-context LINES`: How many unchanged lines to show around changes (default: 3)
* `--diff-output FILE`: Save the diff to a file instead of showing on screen

### Configuration Management

Tired of typing the same options every time? Save your favorite settings for quick reuse!

### Saving Configuration

Just add the `--save-config` flag to any command:

* **Save to the default location:**
  ```bash
  promptprep -d ./my_project --summary-mode --metadata --save-config
  ```
  This stores your settings in `~/.promptprep/config.json`

* **Save to a custom file:**
  ```bash
  promptprep -d ./my_project --format markdown --save-config my_settings.json
  ```

When you use `--save-config` on its own, PromptPrep will save your settings and then exit.

### Loading Configuration

Use the `--load-config` flag to apply saved settings. You can still add new options to override specific settings:

* **Load from the default location:**
  ```bash
  promptprep --load-config -o new_output.txt
  ```
  This loads from `~/.promptprep/config.json` but uses a different output file

* **Load from a custom file:**
  ```bash
  promptprep --load-config my_settings.json
  ```

### Default Location

PromptPrep stores configurations in `~/.promptprep/config.json` unless you specify another path.

Key Concepts Explained
----------------------

Let me walk you through the main ideas behind PromptPrep:

### File Aggregation

This is the heart of PromptPrep: it gathers code from multiple files and combines them into one neat package. Think of it like stapling all your important papers together, but smarter - it adds headers and formats everything nicely.

### Directory Tree

Ever tried to explain your project structure to someone? The ASCII directory tree gives you a visual map showing folders and files, making it easy to understand how everything fits together. It looks something like this:

```
project/
├── src/
│   ├── main.py
│   └── utils.py
└── tests/
    └── test_main.py
```

### Interactive Mode (TUI)

Typing long paths is no fun. The interactive Terminal User Interface lets you browse and select files visually:
* Use **arrow keys** to navigate folders
* Press **Enter/Space** to select or deselect files
* Press **t** to show/hide hidden files
* Press **a** to select everything in a directory
* Press **s** to save your selection and continue
* Press **q** to quit

### Summary Mode

Sometimes you just want the big picture. Summary mode gives you just function and class definitions along with their docstrings - perfect for understanding a codebase's structure without diving into implementation details.

### Incremental Processing

Why reprocess everything when only a few files changed? With `--incremental` and a timestamp, PromptPrep only processes files that have been modified since your last run. This is a huge timesaver for big projects!

### Diff Generation

The `--diff` option lets you compare different versions of your codebase. It highlights lines that were added, removed, or changed, making it easy to track what's new or different between versions.

### Metadata & Token Counting

* **Metadata** gives you useful stats about your code: how many files, total lines, code vs. comments ratio, etc.
* **Token Counting** estimates how many tokens your code will use when sent to AI models like GPT-4, helping you stay within context limits.

Output Formats
--------------

You can choose how your output looks with the `--format` option:

### Available Formats

* **`plain` (Default):** Simple text format with clear file headers. Clean, straightforward, and works everywhere.

* **`markdown`:** Perfect for GitHub or documentation sites. Your code gets proper syntax highlighting in Markdown code blocks (like ````python`), and metadata appears in a nice table.

* **`html`:** Creates a complete webpage with your code. The HTML file is self-contained with CSS styling, so you can open it directly in any browser.

* **`highlighted`:** The prettiest option! Adds full syntax highlighting with colors to make your code more readable. Needs the optional `pygments` package (`pip install .[highlighting]`).

* **`custom`:** Ultimate flexibility - design your own output format using a template file. See [Custom Templates](#custom-templates) below.

### Selecting a Format

```bash
promptprep --format markdown -o output.md
promptprep --format html -o output.html
promptprep --format highlighted -o output_highlighted.html
promptprep --format custom --template-file my_template.txt -o custom_output.txt
```

Don't worry about file extensions - PromptPrep automatically adjusts them to match the format (e.g., `.md` for markdown, `.html` for HTML formats).

Custom Templates
----------------

Want total control over how your output looks? The custom template feature has you covered!

### Using Custom Templates

It's easy to get started:

1. Create a template file (like `my_template.txt`)
2. Add placeholders (special tags) where you want different parts of your code to appear
3. Run PromptPrep with:
   ```bash
   promptprep -d . --format custom --template-file my_template.txt -o my_output.txt
   ```

### Available Placeholders

Drop these special tags into your template file and PromptPrep will replace them with the actual content:

* `${TITLE}`: The project title (e.g., "Code Aggregation - MyProject")
* `${DIRECTORY_TREE}`: Your ASCII directory structure visualization
* `${METADATA}`: Stats about your code (only if you use `--metadata`)
* `${SKIPPED_FILES}`: List of any files that were too large to include
* `${FILES}`: All your code files with their headers
* `${FILE_HEADER:path/to/file.py}`: Header for a specific file
* `${FILE_CONTENT:path/to/file.py}`: Content of a specific file

This lets you create highly customized reports with exactly the information you want in the order you want it.

### Example Template

Here's a simple template to get you started:

```
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
```

Feel free to modify this to suit your specific needs!

Configuration Management
------------------------

Tired of typing the same options every time? Save your favorite settings for quick reuse!

### Saving Configuration

Just add the `--save-config` flag to any command:

* **Save to the default location:**
  ```bash
  promptprep -d ./my_project --summary-mode --metadata --save-config
  ```
  This stores your settings in `~/.promptprep/config.json`

* **Save to a custom file:**
  ```bash
  promptprep -d ./my_project --format markdown --save-config my_settings.json
  ```

When you use `--save-config` on its own, PromptPrep will save your settings and then exit.

### Loading Configuration

Use the `--load-config` flag to apply saved settings. You can still add new options to override specific settings:

* **Load from the default location:**
  ```bash
  promptprep --load-config -o new_output.txt
  ```
  This loads from `~/.promptprep/config.json` but uses a different output file

* **Load from a custom file:**
  ```bash
  promptprep --load-config my_settings.json
  ```

### Default Location

PromptPrep stores configurations in `~/.promptprep/config.json` unless you specify another path.

Testing
-------

The project includes a comprehensive test suite using `pytest`.

1.  Make sure you have installed the development dependencies.
2.  Navigate to the project's root directory.
3.  Run the tests:
    
        pytest
    

Contributing
------------

I'd love your help making PromptPrep even better! Here's how you can contribute:

1. **Fork** the repository on GitHub
2. **Clone** your fork and create a new **branch** for your feature (`git checkout -b cool-new-feature`)
3. **Code** your improvements or fixes
4. **Add tests** to make sure your code works as expected
5. **Run tests** to make sure everything passes (`pytest`)
6. **Format** your code with Black (`black .`)
7. **Commit** your changes with a descriptive message
8. **Push** to your branch
9. Create a **Pull Request** so I can review your changes

Your code should follow the project's style and include proper documentation and tests. If you're not sure where to start, check out the open issues!

License
-------

PromptPrep is licensed under the **MIT License**, so you can freely use, modify, and distribute it. See the `LICENSE` file for the complete legal text.
