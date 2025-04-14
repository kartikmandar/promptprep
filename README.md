<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PromptPrep README</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            margin: 20px;
            padding: 0;
            color: #333;
        }
        h1, h2, h3 {
            color: #2c3e50;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            border-bottom: 1px solid #eee;
            padding-bottom: 0.3em;
        }
        h1 { font-size: 2em; }
        h2 { font-size: 1.5em; }
        h3 { font-size: 1.2em; }
        p { margin-bottom: 1em; }
        ul, ol { margin-left: 20px; margin-bottom: 1em; }
        li { margin-bottom: 0.5em; }
        code {
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
            background-color: #f1f1f1;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-size: 85%;
        }
        pre {
            background-color: #f6f8fa;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
            font-size: 85%;
            line-height: 1.45;
            margin-bottom: 1em;
        }
        pre code {
            padding: 0;
            background-color: transparent;
            border-radius: 0;
        }
        a {
            color: #0366d6;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        img { max-width: 100%; }
        blockquote {
            padding: 0 1em;
            color: #6a737d;
            border-left: 0.25em solid #dfe2e5;
            margin-left: 0;
            margin-right: 0;
        }
        hr {
            height: 0.25em;
            padding: 0;
            margin: 24px 0;
            background-color: #e1e4e8;
            border: 0;
        }
        table {
            border-collapse: collapse;
            margin-bottom: 1em;
            width: auto;
            display: block;
            overflow: auto;
        }
        th, td {
            border: 1px solid #dfe2e5;
            padding: 6px 13px;
        }
        th { font-weight: 600; }
        tr { background-color: #fff; border-top: 1px solid #c6cbd1; }
        tr:nth-child(2n) { background-color: #f6f8fa; }
    </style>
</head>
<body>

<h1>PromptPrep</h1>

<p>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python Version"></a>
</p>

<h2>Table of Contents</h2>
<ul>
    <li><a href="#promptprep">PromptPrep</a>
        <ul>
            <li><a href="#table-of-contents">Table of Contents</a></li>
            <li><a href="#overview">Overview</a></li>
            <li><a href="#features">Features</a></li>
            <li><a href="#installation">Installation</a>
                <ul>
                    <li><a href="#prerequisites">Prerequisites</a></li>
                    <li><a href="#from-source">From Source</a></li>
                    <li><a href="#optional-features">Optional Features</a></li>
                </ul>
            </li>
            <li><a href="#usage">Usage</a>
                <ul>
                    <li><a href="#basic-command">Basic Command</a></li>
                    <li><a href="#common-options">Common Options</a></li>
                    <li><a href="#example-commands">Example Commands</a></li>
                </ul>
            </li>
            <li><a href="#command-line-reference">Command-Line Reference</a>
                <ul>
                    <li><a href="#core-options">Core Options</a></li>
                    <li><a href="#file-selection--filtering">File Selection & Filtering</a></li>
                    <li><a href="#content-processing">Content Processing</a></li>
                    <li><a href="#output-formatting">Output Formatting</a></li>
                    <li><a href="#incremental-processing">Incremental Processing</a></li>
                    <li><a href="#file-comparison-diff">File Comparison (Diff)</a></li>
                    <li><a href="#configuration-management">Configuration Management</a></li>
                </ul>
            </li>
            <li><a href="#key-concepts-explained">Key Concepts Explained</a>
                <ul>
                    <li><a href="#file-aggregation">File Aggregation</a></li>
                    <li><a href="#directory-tree">Directory Tree</a></li>
                    <li><a href="#interactive-mode-tui">Interactive Mode (TUI)</a></li>
                    <li><a href="#summary-mode">Summary Mode</a></li>
                    <li><a href="#incremental-processing-1">Incremental Processing</a></li>
                    <li><a href="#diff-generation">Diff Generation</a></li>
                    <li><a href="#metadata--token-counting">Metadata & Token Counting</a></li>
                </ul>
            </li>
            <li><a href="#output-formats">Output Formats</a>
                <ul>
                    <li><a href="#available-formats">Available Formats</a></li>
                    <li><a href="#selecting-a-format">Selecting a Format</a></li>
                </ul>
            </li>
            <li><a href="#custom-templates">Custom Templates</a>
                <ul>
                    <li><a href="#using-custom-templates">Using Custom Templates</a></li>
                    <li><a href="#available-placeholders">Available Placeholders</a></li>
                    <li><a href="#example-template">Example Template</a></li>
                </ul>
            </li>
            <li><a href="#configuration-management-1">Configuration Management</a>
                <ul>
                    <li><a href="#saving-configuration">Saving Configuration</a></li>
                    <li><a href="#loading-configuration">Loading Configuration</a></li>
                    <li><a href="#default-location">Default Location</a></li>
                </ul>
            </li>
            <li><a href="#testing">Testing</a></li>
            <li><a href="#contributing">Contributing</a></li>
            <li><a href="#license">License</a></li>
        </ul>
    </li>
</ul>

<h2 id="overview">Overview</h2>

<p><strong>PromptPrep</strong> is a versatile command-line tool designed to consolidate code from multiple files within a project into a single, well-structured output file. It intelligently generates an ASCII representation of your directory structure and concatenates the content of selected files, making it ideal for various tasks:</p>

<ul>
    <li><strong>Preparing Code for AI Models:</strong> Easily package your relevant codebase to provide context for Large Language Models (LLMs) like GPT-4 for analysis, code generation, or debugging assistance.</li>
    <li><strong>Codebase Documentation:</strong> Create a snapshot of your project's structure and code for documentation or sharing purposes.</li>
    <li><strong>Project Analysis:</strong> Generate summaries or gather metadata (like lines of code, comment ratios, token counts) across your project for quick insights.</li>
    <li><strong>Code Review:</strong> Share a consolidated view of changes or specific parts of a project.</li>
</ul>

<p>It offers fine-grained control over file selection, content processing, and output formatting to suit your specific needs.</p>

<h2 id="features">Features</h2>

<p>PromptPrep comes packed with features to streamline your code aggregation workflow:</p>

<ul>
    <li><strong>Code Aggregation:</strong> Merges content from multiple source files into one output.</li>
    <li><strong>Directory Tree Generation:</strong> Automatically includes an ASCII tree visualizing the project structure.</li>
    <li><strong>Flexible File Selection:</strong>
        <ul>
            <li>Specify include/exclude patterns for files and directories.</li>
            <li>Filter by file extensions (uses a comprehensive default list or your custom set).</li>
            <li>Set maximum file size limits to skip overly large files.</li>
            <li>Exclude specific file names (like the output file itself).</li>
        </ul>
    </li>
    <li><strong>Interactive TUI Mode:</strong> A terminal-based interface (<code>curses</code>) to visually browse and select/deselect files and directories.</li>
    <li><strong>Content Processing Options:</strong>
        <ul>
            <li><strong>Summary Mode:</strong> Extracts only class/function definitions and their docstrings for a high-level view.</li>
            <li><strong>Comment Filtering:</strong> Option to include or completely exclude comments from the output.</li>
            <li><strong>Line Numbering:</strong> Prepend line numbers to code blocks.</li>
        </ul>
    </li>
    <li><strong>Multiple Output Formats:</strong>
        <ul>
            <li><code>plain</code>: Simple text output (default).</li>
            <li><code>markdown</code>: GitHub-Flavored Markdown with code blocks.</li>
            <li><code>html</code>: A self-contained HTML document with basic styling.</li>
            <li><code>highlighted</code>: Syntax-highlighted output (HTML or terminal ANSI codes) using <code>pygments</code> (optional dependency).</li>
            <li><code>custom</code>: Define your own output structure using a template file.</li>
        </ul>
    </li>
    <li><strong>Metadata Collection:</strong> Gathers statistics like total files, lines of code (total, code, comments, blank), and comment ratios.</li>
    <li><strong>Token Counting:</strong> Estimates the token count of the generated output using <code>tiktoken</code> (useful for AI prompt limits).</li>
    <li><strong>Incremental Processing:</strong> Optimize subsequent runs by only processing files modified since a specified timestamp.</li>
    <li><strong>Diff Generation:</strong> Compare the current aggregation output against a previous version to see changes.</li>
    <li><strong>Configuration Management:</strong> Save your preferred command-line options to a JSON file and load them for future use.</li>
    <li><strong>Clipboard Output:</strong> Directly copy the aggregated content to the system clipboard.</li>
</ul>

<h2 id="installation">Installation</h2>

<h3 id="prerequisites">Prerequisites</h3>

<ul>
    <li>Python 3.7 or higher</li>
    <li><code>pip</code> (Python package installer)</li>
</ul>

<h3 id="from-source">From Source</h3>

<ol>
    <li><strong>Clone the repository:</strong>
        <pre><code class="language-bash">git clone <your-repository-url> # Replace with your repo URL
cd promptprep</code></pre>
    </li>
    <li><strong>Install the package:</strong>
        <pre><code class="language-bash">pip install .</code></pre>
    </li>
    <li><strong>For development (editable install):</strong>
        <p>This allows you to modify the code and have the changes reflected immediately without reinstalling.</p>
        <pre><code class="language-bash">pip install -e .</code></pre>
    </li>
</ol>

<h3 id="optional-features">Optional Features</h3>

<ul>
    <li><strong>Syntax Highlighting:</strong> To enable the <code>highlighted</code> output format, install the <code>pygments</code> library:
        <pre><code class="language-bash">pip install .[highlighting]
# Or install all optional dependencies:
# pip install .[all]</code></pre>
        <em>Note: Token counting (<code>tiktoken</code>) and progress bars (<code>tqdm</code>) are installed by default.</em>
    </li>
</ul>

<h2 id="usage">Usage</h2>

<h3 id="basic-command">Basic Command</h3>

<p>The core command structure is:</p>
<pre><code class="language-bash">promptprep [options]</code></pre>
<p>By default, it processes the current directory (<code>.</code>) and saves the output to <code>full_code.txt</code>.</p>

<h3 id="common-options">Common Options</h3>

<ul>
    <li><code>-d, --directory DIR</code>: Specify the root directory to process (default: current directory).</li>
    <li><code>-o, --output-file FILE</code>: Set the name for the output file (default: <code>full_code.txt</code>).</li>
    <li><code>-c, --clipboard</code>: Copy output directly to the clipboard instead of saving to a file.</li>
    <li><code>-i, --include-files LIST</code>: Comma-separated list of file paths (relative to <code>-d</code>) to <em>exclusively</em> include.</li>
    <li><code>-e, --exclude-dirs LIST</code>: Comma-separated list of directory names to exclude (e.g., <code>node_modules,__pycache__</code>). Overrides defaults if provided.</li>
    <li><code>-x, --extensions LIST</code>: Comma-separated list of file extensions (e.g., <code>.py,.js,.html</code>) to include. Overrides defaults if provided.</li>
    <li><code>--format FORMAT</code>: Choose the output style (<code>plain</code>, <code>markdown</code>, <code>html</code>, <code>highlighted</code>, <code>custom</code>).</li>
    <li><code>--interactive</code>: Start the interactive Terminal User Interface (TUI) for file selection.</li>
</ul>

<h3 id="example-commands">Example Commands</h3>

<ol>
    <li><strong>Aggregate current directory to <code>output.txt</code>:</strong>
        <pre><code class="language-bash">promptprep -o output.txt</code></pre>
    </li>
    <li><strong>Process a specific project folder:</strong>
        <pre><code class="language-bash">promptprep -d ./my_project -o project_code.md --format markdown</code></pre>
    </li>
    <li><strong>Generate a summary with metadata, excluding comments:</strong>
        <pre><code class="language-bash">promptprep -d ./src --summary-mode --metadata --no-include-comments -o summary.txt</code></pre>
    </li>
    <li><strong>Include only Python and JS files, excluding <code>dist</code> and <code>.cache</code> folders:</strong>
        <pre><code class="language-bash">promptprep -d . -x ".py,.js" -e "dist,.cache" -o web_code.txt</code></pre>
    </li>
    <li><strong>Use interactive mode to select files, then copy to clipboard:</strong>
        <pre><code class="language-bash">promptprep -d ./my_app --interactive -c</code></pre>
    </li>
    <li><strong>Generate an HTML report with syntax highlighting:</strong>
        <pre><code class="language-bash">promptprep -d . --format highlighted -o report.html
# Ensure you installed the optional dependency: pip install .[highlighting]</code></pre>
    </li>
    <li><strong>Compare current state with a previous run:</strong>
        <pre><code class="language-bash"># First run (or save a previous state)
promptprep -d . -o project_v1.txt
# Make changes to the code...
# Compare
promptprep --diff project_v1.txt -o project_v2.txt</code></pre>
    </li>
</ol>

<h2 id="command-line-reference">Command-Line Reference</h2>

<p>Here's a detailed breakdown of all available command-line options:</p>

<h3 id="core-options">Core Options</h3>
<ul>
    <li><code>-d, --directory DIR</code>: Directory to process (default: current working directory).</li>
    <li><code>-o, --output-file FILE</code>: Output file name (default: <code>full_code.txt</code>). The extension might be adjusted based on the chosen <code>--format</code>.</li>
    <li><code>-c, --clipboard</code>: Copy output to clipboard instead of writing to a file. Overrides <code>-o</code>.</li>
</ul>

<h3 id="file-selection--filtering">File Selection & Filtering</h3>
<ul>
    <li><code>-i, --include-files LIST</code>: Comma-separated list of <em>relative</em> file paths to include. If specified, <em>only</em> these files are considered.</li>
    <li><code>-e, --exclude-dirs LIST</code>: Comma-separated list of directory names to exclude (e.g., <code>venv,node_modules</code>). Overrides default exclusions if provided.</li>
    <li><code>-x, --extensions LIST</code>: Comma-separated list of file extensions (with leading dot, e.g., <code>.py,.java</code>) to include. Overrides default extensions if provided.</li>
    <li><code>-m, --max-file-size MB</code>: Maximum file size in Megabytes to include (default: 100.0). Larger files are skipped.</li>
    <li><code>--interactive</code>: Launch the Terminal User Interface (TUI) for interactive file/directory selection.</li>
</ul>

<h3 id="content-processing">Content Processing</h3>
<ul>
    <li><code>--summary-mode</code>: Only include function/class definitions and their docstrings.</li>
    <li><code>--include-comments</code>: Include comments in the output (default behavior).</li>
    <li><code>--no-include-comments</code>: Exclude comments from the output. Takes precedence over <code>--include-comments</code>.</li>
    <li><code>--metadata</code>: Include a metadata section with codebase statistics (lines, files, comment ratio).</li>
    <li><code>--count-tokens</code>: Count estimated tokens using <code>tiktoken</code> and include in metadata (requires <code>--metadata</code>).</li>
    <li><code>--token-model MODEL</code>: Specify the <code>tiktoken</code> model for counting (default: <code>cl100k_base</code>, suitable for GPT-4).</li>
</ul>

<h3 id="output-formatting">Output Formatting</h3>
<ul>
    <li><code>--format FORMAT</code>: Output format. Choices: <code>plain</code> (default), <code>markdown</code>, <code>html</code>, <code>highlighted</code>, <code>custom</code>.</li>
    <li><code>--line-numbers</code>: Add line numbers to the code content sections.</li>
    <li><code>--template-file FILE</code>: Path to a custom template file. <strong>Required</strong> if <code>--format custom</code> is used.</li>
</ul>

<h3 id="incremental-processing">Incremental Processing</h3>
<ul>
    <li><code>--incremental</code>: Process only files modified since the timestamp specified by <code>--last-run-timestamp</code>.</li>
    <li><code>--last-run-timestamp TS</code>: Unix timestamp (seconds since epoch, e.g., <code>1678886400.0</code>) indicating the time of the last run. Needed for <code>--incremental</code>.</li>
</ul>

<h3 id="file-comparison-diff">File Comparison (Diff)</h3>
<ul>
    <li><code>--diff PREV_FILE</code>: Compare the output of the current run settings against the content of <code>PREV_FILE</code>. Instead of generating a full aggregation, it outputs a diff.</li>
    <li><code>--diff-context LINES</code>: Number of context lines to show around changes in the diff (default: 3).</li>
    <li><code>--diff-output FILE</code>: Save the generated diff to <code>FILE</code> instead of printing it to the console.</li>
</ul>

<h3 id="configuration-management">Configuration Management</h3>
<ul>
    <li><code>--save-config [CONFIG_FILE]</code>: Save the current command-line arguments (excluding <code>--save-config</code> and <code>--load-config</code>) to a JSON file. If <code>CONFIG_FILE</code> is omitted, saves to the default location (<code>~/.promptprep/config.json</code>). Exits after saving if it's the only action.</li>
    <li><code>--load-config [CONFIG_FILE]</code>: Load settings from the specified JSON file before processing other arguments. If <code>CONFIG_FILE</code> is omitted, loads from the default location. Command-line arguments override loaded settings.</li>
</ul>

<h2 id="key-concepts-explained">Key Concepts Explained</h2>

<h3 id="file-aggregation">File Aggregation</h3>
<p>The core function: reading multiple specified source code files and combining their content into a single output stream or file.</p>

<h3 id="directory-tree">Directory Tree</h3>
<p>An ASCII representation of the folder structure within the target directory, showing nested folders and files. Excluded directories are marked.</p>

<h3 id="interactive-mode-tui">Interactive Mode (TUI)</h3>
<p>Uses the <code>curses</code> library to provide a text-based interface in your terminal. You can navigate directories using arrow keys, select/deselect files and folders with Enter/Space, toggle hidden files ('t'), select all files in a directory ('a'), and save ('s') or quit ('q').</p>

<h3 id="summary-mode">Summary Mode</h3>
<p>Instead of including the full content of files, this mode parses Python files (using <code>ast</code>) to extract only <code>class</code> and <code>def</code> signatures along with their docstrings. This provides a concise overview of the code's structure and purpose.</p>

<h3 id="incremental-processing-1">Incremental Processing</h3>
<p>When using <code>--incremental</code> and providing <code>--last-run-timestamp</code>, PromptPrep checks the modification time of each file. Only files modified <em>after</em> the provided timestamp will be included in the aggregation. This significantly speeds up subsequent runs on large projects where only a few files have changed.</p>

<h3 id="diff-generation">Diff Generation</h3>
<p>Using the <code>--diff PREV_FILE</code> option allows you to compare the potential output of the <em>current</em> command settings against a <em>previously generated</em> output file (<code>PREV_FILE</code>). It highlights lines added (<code>+</code>), removed (<code>-</code>), or changed. This is useful for seeing how the aggregated output has evolved between code changes or setting adjustments.</p>

<h3 id="metadata--token-counting">Metadata & Token Counting</h3>
<ul>
    <li><strong>Metadata (<code>--metadata</code>):</strong> Calculates basic statistics about the included files: total lines, lines of code, comment lines, blank lines, number of files, and the ratio of comment lines to code+comment lines.</li>
    <li><strong>Token Counting (<code>--count-tokens</code>):</strong> Uses the <code>tiktoken</code> library (the tokenizer used by OpenAI models) to estimate the number of tokens in the final aggregated output. This helps ensure the output fits within the context window limits of AI models. Requires <code>--metadata</code>.</li>
</ul>

<h2 id="output-formats">Output Formats</h2>

<p>PromptPrep can format the aggregated output in several ways using the <code>--format</code> option.</p>

<h3 id="available-formats">Available Formats</h3>
<ul>
    <li><strong><code>plain</code> (Default):</strong> Simple text output. Files are separated by clear header comments.</li>
    <li><strong><code>markdown</code>:</strong> Formats the output using Markdown. Includes a Markdown table for metadata and uses Markdown code fences (e.g., <code>```python ... ```</code>) for code blocks, inferring the language from the file extension.</li>
    <li><strong><code>html</code>:</strong> Generates a complete, self-contained HTML document with basic CSS styling for readability. Code is placed within <code><pre></code> tags.</li>
    <li><strong><code>highlighted</code>:</strong> Produces syntax-highlighted output. Requires the optional <code>pygments</code> dependency (<code>pip install .[highlighting]</code>). By default, generates HTML output with embedded CSS for highlighting. <em>Note: Terminal-based highlighting might be implicitly used in some contexts but HTML is the primary target for this formatter.</em></li>
    <li><strong><code>custom</code>:</strong> Allows you to define the exact output structure using a template file specified with <code>--template-file</code>.</li>
</ul>

<h3 id="selecting-a-format">Selecting a Format</h3>
<pre><code class="language-bash">promptprep --format markdown -o output.md
promptprep --format html -o output.html
promptprep --format highlighted -o output_highlighted.html
promptprep --format custom --template-file my_template.txt -o custom_output.txt</code></pre>

<h2 id="custom-templates">Custom Templates</h2>

<p>For ultimate control over the output structure, use <code>--format custom</code> along with <code>--template-file</code>.</p>

<h3 id="using-custom-templates">Using Custom Templates</h3>
<ol>
    <li>Create a template file (e.g., <code>my_template.txt</code>).</li>
    <li>Use placeholders (see below) in your template file to indicate where different parts of the aggregated content should go.</li>
    <li>Run PromptPrep with the custom format options:
        <pre><code class="language-bash">promptprep -d . --format custom --template-file my_template.txt -o my_output.txt</code></pre>
    </li>
</ol>

<h3 id="available-placeholders">Available Placeholders</h3>
<p>Your template file can include the following placeholders, which PromptPrep will replace with the corresponding content:</p>
<ul>
    <li><code>${TITLE}</code>: The title for the output (e.g., "Code Aggregation - MyProject").</li>
    <li><code>${DIRECTORY_TREE}</code>: The formatted ASCII directory tree.</li>
    <li><code>${METADATA}</code>: The formatted metadata section (if <code>--metadata</code> is enabled).</li>
    <li><code>${SKIPPED_FILES}</code>: A formatted list of files skipped due to size limits.</li>
    <li><code>${FILES}</code>: A concatenation of all included files, each preceded by its formatted header and followed by its formatted content.</li>
    <li><code>${FILE_HEADER:path/to/file.py}</code>: The formatted header for a <em>specific</em> file (use the relative path).</li>
    <li><code>${FILE_CONTENT:path/to/file.py}</code>: The formatted content for a <em>specific</em> file (use the relative path).</li>
</ul>
<p><em>Note: The formatting of sections like the tree, metadata, headers, and content within the template depends on the base formatter used (defaults to <code>plain</code>, but can be influenced by implementation details).</em></p>

<h3 id="example-template">Example Template</h3>
<pre><code class="language-text"># Project Aggregation: ${TITLE}

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
</code></pre>

<h2 id="configuration-management-1">Configuration Management</h2>

<p>Save and load your preferred command-line settings to avoid retyping them.</p>

<h3 id="saving-configuration">Saving Configuration</h3>
<p>Use the <code>--save-config</code> flag.</p>
<ul>
    <li><strong>Save to default location (<code>~/.promptprep/config.json</code>):</strong>
        <pre><code class="language-bash">promptprep -d ./my_project --summary-mode --metadata --save-config</code></pre>
    </li>
    <li><strong>Save to a specific file:</strong>
        <pre><code class="language-bash">promptprep -d ./my_project --format markdown --save-config my_project_settings.json</code></pre>
        PromptPrep will save the settings used in the command and then exit if saving is the primary action requested.
    </li>
</ul>

<h3 id="loading-configuration">Loading Configuration</h3>
<p>Use the <code>--load-config</code> flag. Settings from the config file are applied first, and then any additional command-line arguments can override them.</p>
<ul>
    <li><strong>Load from default location:</strong>
        <pre><code class="language-bash">promptprep --load-config -o updated_output.txt # Overrides output file from config</code></pre>
    </li>
    <li><strong>Load from a specific file:</strong>
        <pre><code class="language-bash">promptprep --load-config my_project_settings.json</code></pre>
    </li>
</ul>

<h3 id="default-location">Default Location</h3>
<p>The default configuration directory is <code>~/.promptprep/</code> and the default file is <code>config.json</code> within that directory.</p>

<h2 id="testing">Testing</h2>

<p>The project includes a comprehensive test suite using <code>pytest</code>.</p>
<ol>
    <li>Make sure you have installed the development dependencies.</li>
    <li>Navigate to the project's root directory.</li>
    <li>Run the tests:
        <pre><code class="language-bash">pytest</code></pre>
    </li>
</ol>

<h2 id="contributing">Contributing</h2>

<p>Contributions are welcome! Please follow these general steps:</p>
<ol>
    <li><strong>Fork</strong> the repository on GitHub.</li>
    <li>Create a new <strong>branch</strong> for your feature or bug fix (<code>git checkout -b feature/my-new-feature</code>).</li>
    <li>Make your <strong>changes</strong>.</li>
    <li>Add <strong>tests</strong> for your changes.</li>
    <li>Ensure all tests <strong>pass</strong> (<code>pytest</code>).</li>
    <li>Format your code using <strong>Black</strong> (<code>black .</code>).</li>
    <li>Commit your changes (<code>git commit -am 'Add some feature'</code>).</li>
    <li>Push to the branch (<code>git push origin feature/my-new-feature</code>).</li>
    <li>Create a new <strong>Pull Request</strong> on GitHub.</li>
</ol>
<p>Please ensure your code adheres to the project's coding style and includes appropriate documentation and tests.</p>

<h2 id="license">License</h2>

<p>This project is licensed under the <strong>MIT License</strong>. See the <code>LICENSE</code> file (if included in the repository, otherwise assume MIT based on <code>pyproject.toml</code>) for details.</p>

</body>
</html>