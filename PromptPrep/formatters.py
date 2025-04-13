"""Formatters for different output formats in PromptPrep."""
from abc import ABC, abstractmethod
import os
from typing import Dict, Optional, List, Any
import re
import pygments
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.formatters import HtmlFormatter as PygmentsHtmlFormatter, TerminalFormatter


class BaseFormatter(ABC):
    """Base formatter class for all output formats."""
    
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
    """Plain text formatter - the default format."""
    
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
    """Markdown formatter."""
    
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
    """HTML formatter."""
    
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
    """Syntax highlighted code formatter using Pygments."""
    
    def __init__(self, html_output: bool = True):
        """Initialize highlighted formatter.
        
        Args:
            html_output: Whether to output HTML (True) or terminal escape codes (False)
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


def get_formatter(output_format: str = "plain") -> BaseFormatter:
    """Get the appropriate formatter for the specified output format.
    
    Args:
        output_format: The output format name, one of "plain", "markdown", "html", "highlighted"
        
    Returns:
        An instance of the appropriate formatter class
    
    Raises:
        ValueError: If an invalid format is specified
    """
    if output_format == "plain":
        return PlainTextFormatter()
    elif output_format == "markdown":
        return MarkdownFormatter()
    elif output_format == "html":
        return HtmlFormatter()
    elif output_format == "highlighted":
        return HighlightedFormatter()
    else:
        raise ValueError(f"Unknown output format: {output_format}")