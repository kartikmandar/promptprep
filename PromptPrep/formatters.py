"""Makes your code look nice in different output formats."""
from abc import ABC, abstractmethod
import os
from typing import Dict, Optional, List, Any
import re
import string
import pygments
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.formatters import HtmlFormatter as PygmentsHtmlFormatter, TerminalFormatter


class BaseFormatter(ABC):
    """The foundation for all our formatters."""
    
    def __init__(self):
        """Initialize the formatter."""
        pass
    
    @abstractmethod
    def format_directory_tree(self, tree: str) -> str:
        """Format the directory tree."""
        pass
    
    @abstractmethod
    def format_file_header(self, file_path: str) -> str:
        """Format a file header."""
        pass
    
    @abstractmethod
    def format_code_content(self, content: str, file_path: str) -> str:
        """Format code content with line numbers."""
        pass
    
    @abstractmethod
    def format_metadata(self, metadata: Dict[str, Any]) -> str:
        """Format metadata section."""
        pass
    
    @abstractmethod
    def format_error(self, error_msg: str) -> str:
        """Format error messages."""
        pass
    
    @abstractmethod
    def format_skipped_files(self, skipped_files: List[tuple]) -> str:
        """Format skipped files section."""
        pass
    
    def get_file_extension(self, file_path: str) -> str:
        """Get the extension of a file."""
        _, ext = os.path.splitext(file_path)
        return ext.lower()


class PlainTextFormatter(BaseFormatter):
    """Keeps things simple with plain text output."""
    
    def format_directory_tree(self, tree: str) -> str:
        """Format the directory tree in plain text."""
        return f"Directory Tree:\n{tree}\n\n"
    
    def format_file_header(self, file_path: str) -> str:
        """Format a file header in plain text."""
        return (
            f"\n\n# ======================\n"
            f"# File: {file_path}\n"
            f"# ======================\n\n"
        )
    
    def format_code_content(self, content: str, file_path: str) -> str:
        """Format code content in plain text (without line numbers)."""
        # Line numbering is handled by the aggregator based on the flag
        return content
    
    def format_metadata(self, metadata: Dict[str, Any]) -> str:
        """Format metadata section in plain text."""
        result = f"# ======================\n"
        result += f"# Codebase Metadata\n"
        result += f"# ======================\n\n"
        
        for key, value in metadata.items():
            if key == 'comment_ratio' and isinstance(value, float):
                result += f"# {key.replace('_', ' ').title()}: {value:.2f}\n"
            else:
                result += f"# {key.replace('_', ' ').title()}: {value}\n"
        
        return result
    
    def format_error(self, error_msg: str) -> str:
        """Format error messages in plain text."""
        return f"\n# {error_msg}\n"
    
    def format_skipped_files(self, skipped_files: List[tuple]) -> str:
        """Format skipped files section in plain text."""
        if not skipped_files:
            return ""
            
        result = "\n\n# ======================\n"
        result += "# Files skipped due to size limit\n"
        result += "# ======================\n\n"
        
        for file_path, size_mb in skipped_files:
            result += f"# {file_path} ({size_mb:.2f} MB)\n"
        
        return result


class MarkdownFormatter(BaseFormatter):
    """Makes your code look great in Markdown documents."""
    
    def format_directory_tree(self, tree: str) -> str:
        """Format the directory tree in Markdown."""
        # Wrap tree in a code block for proper formatting
        return f"## Directory Tree\n\n```\n{tree}\n```\n\n"
    
    def format_file_header(self, file_path: str) -> str:
        """Format a file header in Markdown."""
        return f"\n\n## File: {file_path}\n\n"
    
    def format_code_content(self, content: str, file_path: str) -> str:
        """Format code content in Markdown (without line numbers)."""
        ext = self.get_file_extension(file_path) or ""
        # Remove the dot from the extension for markdown code blocks
        lang = ext[1:] if ext else ""
        
        # Line numbering is handled by the aggregator based on the flag
        return f"```{lang}\n{content}\n```"
    
    def format_metadata(self, metadata: Dict[str, Any]) -> str:
        """Format metadata section in Markdown."""
        result = "## Codebase Metadata\n\n"
        result += "| Metric | Value |\n"
        result += "| ------ | ----- |\n"
        
        for key, value in metadata.items():
            if key == 'comment_ratio' and isinstance(value, float):
                result += f"| {key.replace('_', ' ').title()} | {value:.2f} |\n"
            else:
                result += f"| {key.replace('_', ' ').title()} | {value} |\n"
        
        return result
    
    def format_error(self, error_msg: str) -> str:
        """Format error messages in Markdown."""
        return f"\n> **Error:** {error_msg}\n"
    
    def format_skipped_files(self, skipped_files: List[tuple]) -> str:
        """Format skipped files section in Markdown."""
        if not skipped_files:
            return ""
            
        result = "\n\n## Files skipped due to size limit\n\n"
        result += "| File | Size |\n"
        result += "| ---- | ---- |\n"
        
        for file_path, size_mb in skipped_files:
            result += f"| {file_path} | {size_mb:.2f} MB |\n"
        
        return result


class HtmlFormatter(BaseFormatter):
    """Creates a nice-looking webpage with your code."""
    
    def __init__(self):
        """Initialize HTML formatter with CSS styles."""
        super().__init__()
        self.css = """
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                color: #333;
                background-color: #f8f8f8;
            }
            h1, h2 {
                color: #2c3e50;
                margin-top: 30px;
                margin-bottom: 15px;
            }
            pre {
                background-color: #f1f1f1;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
                font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
                font-size: 14px;
                white-space: pre-wrap;
            }
            pre.tree {
                font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
            }
            .line-number {
                color: #999;
                margin-right: 10px;
                user-select: none;
            }
            .file-header {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border-radius: 5px 5px 0 0;
                font-weight: bold;
                margin-top: 25px;
            }
            .file-content {
                margin-top: 0;
                border-radius: 0 0 5px 5px;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            .error-message {
                color: #e74c3c;
                padding: 10px;
                margin: 10px 0;
                background-color: #fadbd8;
                border-left: 4px solid #e74c3c;
            }
        </style>
        """
    
    def format_directory_tree(self, tree: str) -> str:
        """Format the directory tree in HTML."""
        escaped_tree = tree.replace("<", "&lt;").replace(">", "&gt;")
        return f"<h2>Directory Tree</h2>\n<pre class='tree'>{escaped_tree}</pre>\n\n"
    
    def format_file_header(self, file_path: str) -> str:
        """Format a file header in HTML."""
        escaped_path = file_path.replace("<", "&lt;").replace(">", "&gt;")
        return f"\n\n<div class='file-header'>File: {escaped_path}</div>\n"
    
    def format_code_content(self, content: str, file_path: str) -> str:
        """Format code content in HTML (without line numbers)."""
        # Line numbering is handled by the aggregator based on the flag
        escaped_content = content.replace("<", "&lt;").replace(">", "&gt;")
        return f"<pre class='file-content'>{escaped_content}</pre>"
    
    def format_metadata(self, metadata: Dict[str, Any]) -> str:
        """Format metadata section in HTML."""
        result = "<h2>Codebase Metadata</h2>\n\n<table>\n"
        result += "<tr><th>Metric</th><th>Value</th></tr>\n"
        
        for key, value in metadata.items():
            if key == 'comment_ratio' and isinstance(value, float):
                result += f"<tr><td>{key.replace('_', ' ').title()}</td><td>{value:.2f}</td></tr>\n"
            else:
                result += f"<tr><td>{key.replace('_', ' ').title()}</td><td>{value}</td></tr>\n"
        
        result += "</table>\n"
        return result
    
    def format_error(self, error_msg: str) -> str:
        """Format error messages in HTML."""
        escaped_msg = error_msg.replace("<", "&lt;").replace(">", "&gt;")
        return f"\n<div class='error-message'>Error: {escaped_msg}</div>\n"
    
    def format_skipped_files(self, skipped_files: List[tuple]) -> str:
        """Format skipped files section in HTML."""
        if not skipped_files:
            return ""
            
        result = "\n\n<h2>Files skipped due to size limit</h2>\n\n<table>\n"
        result += "<tr><th>File</th><th>Size</th></tr>\n"
        
        for file_path, size_mb in skipped_files:
            escaped_path = file_path.replace("<", "&lt;").replace(">", "&gt;")
            result += f"<tr><td>{escaped_path}</td><td>{size_mb:.2f} MB</td></tr>\n"
        
        result += "</table>\n"
        return result
    
    def get_full_html(self, content: str, title: str = "Code Aggregation") -> str:
        """Wrap content in a complete HTML document."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {self.css}
</head>
<body>
    <h1>{title}</h1>
    {content}
</body>
</html>
"""


class HighlightedFormatter(BaseFormatter):
    """Adds syntax highlighting to make your code pop."""
    
    def __init__(self, html_output: bool = True):
        """Gets ready to highlight your code.
        
        Args:
            html_output: True for web pages, False for terminal colors
        """
        super().__init__()
        self.html_output = html_output
        self.pygments_formatter = PygmentsHtmlFormatter(cssclass="source", wrapcode=True) if html_output else TerminalFormatter()
        self.base_formatter = HtmlFormatter() if html_output else PlainTextFormatter()
    
    def format_directory_tree(self, tree: str) -> str:
        """Format the directory tree with highlighting."""
        return self.base_formatter.format_directory_tree(tree)
    
    def format_file_header(self, file_path: str) -> str:
        """Format a file header with highlighting."""
        return self.base_formatter.format_file_header(file_path)
    
    def format_code_content(self, content: str, file_path: str) -> str:
        """Format code content with syntax highlighting (without line numbers)."""
        try:
            lexer = get_lexer_for_filename(file_path, stripall=True)
        except Exception:
            lexer = TextLexer()
        
        # Line numbering is handled by the aggregator based on the flag
        highlighted = highlight(content, lexer, self.pygments_formatter)
        
        # For HTML output, we need to add CSS
        if self.html_output:
            css = self.pygments_formatter.get_style_defs('.source')
            return f"<style>{css}</style>\n{highlighted}"
        
        return highlighted
    
    def format_metadata(self, metadata: Dict[str, Any]) -> str:
        """Format metadata section."""
        return self.base_formatter.format_metadata(metadata)
    
    def format_error(self, error_msg: str) -> str:
        """Format error messages."""
        return self.base_formatter.format_error(error_msg)
    
    def format_skipped_files(self, skipped_files: List[tuple]) -> str:
        """Format skipped files section."""
        return self.base_formatter.format_skipped_files(skipped_files)
    
    def get_full_html(self, content: str, title: str = "Code Aggregation") -> str:
        """Wrap content in a complete HTML document if in HTML mode."""
        if self.html_output and hasattr(self.base_formatter, 'get_full_html'):
            return self.base_formatter.get_full_html(content, title)
        return content


class CustomTemplateFormatter(BaseFormatter):
    """Lets you design your own output format using a template file.
    
    Your template can use these placeholders:
    - ${DIRECTORY_TREE} - Shows your folder structure
    - ${FILE_HEADER:path} - Adds a header for each file
    - ${FILE_CONTENT:path} - Puts in the actual code
    - ${METADATA} - Adds stats about your codebase
    - ${SKIPPED_FILES} - Lists any files that were too big
    - ${FILES} - All your files with headers and content
    - ${TITLE} - The main title
    """

    def __init__(self, template_file: str, base_format: str = "plain"):
        """Initialize custom template formatter.
        
        Args:
            template_file: Path to the template file
            base_format: The base format to use for sections not defined in the template
                         (plain, markdown, html, highlighted)
        """
        super().__init__()
        self.template_file = template_file
        self.template = self._load_template(template_file)
        self.base_format = base_format
        
        # Use a base formatter for basic formatting
        if base_format == "plain":
            self.base_formatter = PlainTextFormatter()
        elif base_format == "markdown":
            self.base_formatter = MarkdownFormatter()
        elif base_format == "html":
            self.base_formatter = HtmlFormatter()
        elif base_format == "highlighted":
            self.base_formatter = HighlightedFormatter()
        else:
            self.base_formatter = PlainTextFormatter()

    def _load_template(self, template_file: str) -> str:
        """Load the template file content."""
        try:
            with open(template_file, 'r') as f:
                return f.read()
        except IOError as e:
            raise IOError(f"Could not read template file: {e}")

    def format_directory_tree(self, tree: str) -> str:
        """Format the directory tree using the base formatter."""
        return self.base_formatter.format_directory_tree(tree)
    
    def format_file_header(self, file_path: str) -> str:
        """Format a file header using the base formatter."""
        return self.base_formatter.format_file_header(file_path)
    
    def format_code_content(self, content: str, file_path: str) -> str:
        """Format code content using the base formatter."""
        return self.base_formatter.format_code_content(content, file_path)
    
    def format_metadata(self, metadata: Dict[str, Any]) -> str:
        """Format metadata section using the base formatter."""
        return self.base_formatter.format_metadata(metadata)
    
    def format_error(self, error_msg: str) -> str:
        """Format error messages using the base formatter."""
        return self.base_formatter.format_error(error_msg)
    
    def format_skipped_files(self, skipped_files: List[tuple]) -> str:
        """Format skipped files section using the base formatter."""
        return self.base_formatter.format_skipped_files(skipped_files)

    def render_template(self, directory_tree: str, files_content: Dict[str, str], 
                       metadata: Dict[str, Any], skipped_files: List[tuple], title: str = "Code Aggregation") -> str:
        """Render the template with the provided content.
        
        Args:
            directory_tree: ASCII representation of the directory tree
            files_content: Dictionary mapping file paths to their content
            metadata: Dictionary of metadata about the codebase
            skipped_files: List of (file_path, size) tuples for skipped files
            title: Title of the output (default: "Code Aggregation")
            
        Returns:
            The rendered template content
        """
        # Start with the template
        result = self.template
        
        # Replace title placeholder
        result = result.replace("${TITLE}", title)
        
        # Replace directory tree placeholder
        if "${DIRECTORY_TREE}" in result:
            formatted_tree = self.format_directory_tree(directory_tree)
            result = result.replace("${DIRECTORY_TREE}", formatted_tree)
        
        # Replace metadata placeholder
        if "${METADATA}" in result:
            formatted_metadata = self.format_metadata(metadata)
            result = result.replace("${METADATA}", formatted_metadata)
        
        # Replace skipped files placeholder
        if "${SKIPPED_FILES}" in result:
            formatted_skipped = self.format_skipped_files(skipped_files)
            result = result.replace("${SKIPPED_FILES}", formatted_skipped)
        
        # Replace file header and content placeholders
        for placeholder_type in ["FILE_HEADER", "FILE_CONTENT"]:
            pattern = re.compile(r'\${' + placeholder_type + r':([^}]+)}')
            matches = pattern.findall(result)
            
            for file_path in matches:
                placeholder = f"${{{placeholder_type}:{file_path}}}"
                
                if file_path in files_content:
                    if placeholder_type == "FILE_HEADER":
                        formatted = self.format_file_header(file_path)
                    else:  # FILE_CONTENT
                        formatted = self.format_code_content(files_content[file_path], file_path)
                    
                    result = result.replace(placeholder, formatted)
                else:
                    error_msg = f"File not found: {file_path}"
                    result = result.replace(placeholder, self.format_error(error_msg))
        
        # Handle generic file placeholders
        if "${FILES}" in result:
            file_content = ""
            for file_path, content in files_content.items():
                file_content += self.format_file_header(file_path)
                file_content += self.format_code_content(content, file_path)
            result = result.replace("${FILES}", file_content)
        
        return result


# Add CustomTemplateFormatter to the get_formatter logic check
def get_formatter(output_format: str = "plain", template_file: Optional[str] = None,
                 base_format: str = "plain") -> BaseFormatter:
    """Picks the right formatter for your needs.

    Args:
        output_format: How you want it to look (plain, markdown, html, highlighted, custom)
        template_file: Your template file (needed for custom format)
        base_format: Backup format for custom templates (defaults to plain)

    Returns:
        The formatter that'll do the job

    Raises:
        ValueError: If format is unknown or template is missing when needed
    """
    if output_format == "plain":
        return PlainTextFormatter()
    elif output_format == "markdown":
        return MarkdownFormatter()
    elif output_format == "html":
        return HtmlFormatter()
    elif output_format == "highlighted":
        # Decide HTML vs terminal based on some logic or default?
        # For CLI, terminal (False) might be better unless output is piped/redirected.
        # Let's default to terminal highlighting for now if not HTML file.
        # This part might need refinement based on desired behavior.
        # For simplicity, let's assume highlighted implies terminal for non-HTML output.
        # A better approach might be a separate flag or inferring from output file extension.
        # Sticking to the original logic for now:
        return HighlightedFormatter() # Defaults to HTML=True based on original code
    elif output_format == "custom":
        if not template_file:
            raise ValueError("template_file is required for custom output format")
        try:
            # Pass base_format if needed by CustomTemplateFormatter constructor
            return CustomTemplateFormatter(template_file, base_format=base_format)
        except IOError as e:
             raise ValueError(f"Error loading template file: {e}") # Raise ValueError for CLI handling
    else:
        raise ValueError(f"Unknown output format: {output_format}")