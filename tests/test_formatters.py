import os
import re
import pytest
from unittest import mock

from promptprep.formatters import (
    BaseFormatter,
    PlainTextFormatter,
    MarkdownFormatter,
    HtmlFormatter,
    HighlightedFormatter,
    CustomTemplateFormatter,
    get_formatter
)

# Test data
TEST_TREE = "root/\n  file1.py\n  file2.py\n  dir1/\n    file3.py"
TEST_FILE_PATH = "path/to/file.py"
TEST_CONTENT = "def test_function():\n    return True"
TEST_METADATA = {
    "total_files": 10,
    "total_lines": 1000,
    "comment_ratio": 0.25,
    "token_count": 5000
}
TEST_ERROR = "Test error message"
TEST_SKIPPED_FILES = [
    ("large_file.py", 150.5),
    ("another_large_file.rb", 200.25)
]

def test_get_formatter():
    """Test getting formatters by name."""
    # Test all valid formatters
    assert isinstance(get_formatter("plain"), PlainTextFormatter)
    assert isinstance(get_formatter("markdown"), MarkdownFormatter)
    assert isinstance(get_formatter("html"), HtmlFormatter)
    assert isinstance(get_formatter("highlighted"), HighlightedFormatter)
    
    # Test invalid formatter
    with pytest.raises(ValueError) as excinfo:
        get_formatter("invalid")
    assert "Unknown output format: invalid" in str(excinfo.value)

class TestPlainTextFormatter:
    """Tests for PlainTextFormatter."""
    
    def setup_method(self):
        self.formatter = PlainTextFormatter()
    
    def test_format_directory_tree(self):
        """Test formatting directory tree in plain text."""
        result = self.formatter.format_directory_tree(TEST_TREE)
        assert "Directory Tree:" in result
        assert TEST_TREE in result
    
    def test_format_file_header(self):
        """Test formatting file header in plain text."""
        result = self.formatter.format_file_header(TEST_FILE_PATH)
        assert f"File: {TEST_FILE_PATH}" in result
        assert "# ======================" in result  # Changed from "=======================" to "# ======================"
    
    def test_format_code_content(self):
        """Test formatting code content in plain text."""
        result = self.formatter.format_code_content(TEST_CONTENT, TEST_FILE_PATH)
        assert result == TEST_CONTENT  # No modification in plain text format
    
    def test_format_metadata(self):
        """Test formatting metadata in plain text."""
        result = self.formatter.format_metadata(TEST_METADATA)
        assert "Codebase Metadata" in result
        assert "Total Files: 10" in result
        assert "Comment Ratio: 0.25" in result  # Formatted with 2 decimal places
        assert "Token Count: 5000" in result
    
    def test_format_error(self):
        """Test formatting error message in plain text."""
        result = self.formatter.format_error(TEST_ERROR)
        assert TEST_ERROR in result
        assert result.startswith("\n# ")
    
    def test_format_skipped_files(self):
        """Test formatting skipped files in plain text."""
        result = self.formatter.format_skipped_files(TEST_SKIPPED_FILES)
        assert "Files skipped due to size limit" in result
        assert "large_file.py (150.50 MB)" in result
        assert "another_large_file.rb (200.25 MB)" in result
    
    def test_format_skipped_files_empty(self):
        """Test formatting empty skipped files list."""
        result = self.formatter.format_skipped_files([])
        assert result == ""
    
    def test_get_file_extension(self):
        """Test getting file extension."""
        assert self.formatter.get_file_extension("file.py") == ".py"
        assert self.formatter.get_file_extension("file.txt") == ".txt"
        assert self.formatter.get_file_extension("file") == ""
        assert self.formatter.get_file_extension("file.PY") == ".py"  # Case insensitive


class TestMarkdownFormatter:
    """Tests for MarkdownFormatter."""
    
    def setup_method(self):
        self.formatter = MarkdownFormatter()
    
    def test_format_directory_tree(self):
        """Test formatting directory tree in markdown."""
        result = self.formatter.format_directory_tree(TEST_TREE)
        assert "## Directory Tree" in result
        assert "```" in result  # Code block
        assert TEST_TREE in result
    
    def test_format_file_header(self):
        """Test formatting file header in markdown."""
        result = self.formatter.format_file_header(TEST_FILE_PATH)
        assert f"## File: {TEST_FILE_PATH}" in result
    
    def test_format_code_content(self):
        """Test formatting code content in markdown."""
        result = self.formatter.format_code_content(TEST_CONTENT, TEST_FILE_PATH)
        assert result.startswith("```py")  # Code block with language
        assert TEST_CONTENT in result
        assert result.endswith("```")
    
    def test_format_code_content_no_extension(self):
        """Test formatting code content without file extension."""
        result = self.formatter.format_code_content(TEST_CONTENT, "script")
        assert result.startswith("```")  # Code block without language
        assert TEST_CONTENT in result
    
    def test_format_metadata(self):
        """Test formatting metadata in markdown."""
        result = self.formatter.format_metadata(TEST_METADATA)
        assert "## Codebase Metadata" in result
        assert "| Metric | Value |" in result  # Table header
        assert "| Total Files | 10 |" in result
        assert "| Comment Ratio | 0.25 |" in result
    
    def test_format_error(self):
        """Test formatting error message in markdown."""
        result = self.formatter.format_error(TEST_ERROR)
        assert f"**Error:** {TEST_ERROR}" in result
        assert result.startswith("\n> ")  # Blockquote
    
    def test_format_skipped_files(self):
        """Test formatting skipped files in markdown."""
        result = self.formatter.format_skipped_files(TEST_SKIPPED_FILES)
        assert "## Files skipped due to size limit" in result
        assert "| File | Size |" in result  # Table header
        assert "| large_file.py | 150.50 MB |" in result
    
    def test_format_skipped_files_empty(self):
        """Test formatting empty skipped files list."""
        result = self.formatter.format_skipped_files([])
        assert result == ""


class TestHtmlFormatter:
    """Tests for HtmlFormatter."""
    
    def setup_method(self):
        self.formatter = HtmlFormatter()
    
    def test_init(self):
        """Test HTML formatter initialization."""
        assert hasattr(self.formatter, 'css')
        assert "<style>" in self.formatter.css
    
    def test_format_directory_tree(self):
        """Test formatting directory tree in HTML."""
        result = self.formatter.format_directory_tree(TEST_TREE)
        assert "<h2>Directory Tree</h2>" in result
        assert "<pre class='tree'>" in result
        assert TEST_TREE in result
    
    def test_format_directory_tree_escaping(self):
        """Test HTML escaping in directory tree."""
        tree_with_html = "root/\n  <script>alert('test')</script>"
        result = self.formatter.format_directory_tree(tree_with_html)
        assert "<script>" not in result
        assert "&lt;script&gt;" in result  # Escaped
    
    def test_format_file_header(self):
        """Test formatting file header in HTML."""
        result = self.formatter.format_file_header(TEST_FILE_PATH)
        assert "<div class='file-header'" in result
        assert f"File: {TEST_FILE_PATH}" in result
    
    def test_format_file_header_escaping(self):
        """Test HTML escaping in file header."""
        path_with_html = "path/to/<script>file.js</script>"
        result = self.formatter.format_file_header(path_with_html)
        assert "<script>" not in result
        assert "&lt;script&gt;" in result  # Escaped
    
    def test_format_code_content(self):
        """Test formatting code content in HTML."""
        result = self.formatter.format_code_content(TEST_CONTENT, TEST_FILE_PATH)
        assert "<pre class='file-content'>" in result
        assert TEST_CONTENT in result
    
    def test_format_code_content_escaping(self):
        """Test HTML escaping in code content."""
        code_with_html = "def test():\n  print('<script>')"
        result = self.formatter.format_code_content(code_with_html, TEST_FILE_PATH)
        assert "<script>" not in result
        assert "&lt;script&gt;" in result  # Escaped
    
    def test_format_metadata(self):
        """Test formatting metadata in HTML."""
        result = self.formatter.format_metadata(TEST_METADATA)
        assert "<h2>Codebase Metadata</h2>" in result
        assert "<table>" in result
        assert "<tr><th>Metric</th><th>Value</th></tr>" in result
        assert "<tr><td>Total Files</td><td>10</td></tr>" in result
    
    def test_format_error(self):
        """Test formatting error message in HTML."""
        result = self.formatter.format_error(TEST_ERROR)
        assert "<div class='error-message'" in result
        assert f"Error: {TEST_ERROR}" in result
    
    def test_format_error_escaping(self):
        """Test HTML escaping in error message."""
        error_with_html = "Error: <script>alert('error')</script>"
        result = self.formatter.format_error(error_with_html)
        assert "<script>" not in result
        assert "&lt;script&gt;" in result  # Escaped
    
    def test_format_skipped_files(self):
        """Test formatting skipped files in HTML."""
        result = self.formatter.format_skipped_files(TEST_SKIPPED_FILES)
        assert "<h2>Files skipped due to size limit</h2>" in result
        assert "<table>" in result
        assert "<tr><th>File</th><th>Size</th></tr>" in result
        assert "<tr><td>large_file.py</td><td>150.50 MB</td></tr>" in result
    
    def test_format_skipped_files_empty(self):
        """Test formatting empty skipped files list."""
        result = self.formatter.format_skipped_files([])
        assert result == ""
    
    def test_get_full_html(self):
        """Test getting full HTML document."""
        content = "<p>Test content</p>"
        title = "Test Title"
        result = self.formatter.get_full_html(content, title)
        assert "<!DOCTYPE html>" in result
        assert "<html lang=\"en\">" in result
        assert f"<title>{title}</title>" in result
        assert content in result
        assert self.formatter.css in result


class TestHighlightedFormatter:
    """Tests for HighlightedFormatter."""
    
    def setup_method(self):
        self.html_formatter = HighlightedFormatter(html_output=True)
        self.terminal_formatter = HighlightedFormatter(html_output=False)
    
    def test_init(self):
        """Test highlighted formatter initialization."""
        assert self.html_formatter.html_output is True
        assert self.terminal_formatter.html_output is False
        assert hasattr(self.html_formatter, 'pygments_formatter')
        assert hasattr(self.terminal_formatter, 'pygments_formatter')
    
    def test_format_directory_tree(self):
        """Test formatting directory tree."""
        # HTML formatter should use HTML formatter's directory tree format
        html_result = self.html_formatter.format_directory_tree(TEST_TREE)
        assert "<h2>Directory Tree</h2>" in html_result
        
        # Terminal formatter should use plain text formatter's directory tree format
        terminal_result = self.terminal_formatter.format_directory_tree(TEST_TREE)
        assert "Directory Tree:" in terminal_result
    
    def test_format_file_header(self):
        """Test formatting file header."""
        # HTML formatter should use HTML formatter's file header format
        html_result = self.html_formatter.format_file_header(TEST_FILE_PATH)
        assert "<div class='file-header'" in html_result
        
        # Terminal formatter should use plain text formatter's file header format
        terminal_result = self.terminal_formatter.format_file_header(TEST_FILE_PATH)
        assert "# ======================" in terminal_result
    
    @pytest.mark.parametrize("filename, content", [
        ("test.py", "def test(): pass"),
        ("test.js", "function test() { return true; }"),
        ("unknown.xyz", "Unknown content type")
    ])
    def test_format_code_content(self, filename, content):
        """Test formatting code content with syntax highlighting."""
        # HTML formatter
        html_result = self.html_formatter.format_code_content(content, filename)
        assert "<style>" in html_result
        assert "class=" in html_result  # Pygments adds class attributes
        
        # Terminal formatter - strip ANSI codes for comparison
        # ANSI codes pattern: ESC[...m
        terminal_result = self.terminal_formatter.format_code_content(content, filename)
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        plain_result = ansi_escape.sub('', terminal_result)
        
        # Check if the actual content is present (ignoring ANSI styling)
        clean_content = content.replace(" ", "").replace("\n", "")
        clean_result = plain_result.replace(" ", "").replace("\n", "")
        assert clean_content in clean_result
    
    def test_format_metadata(self):
        """Test formatting metadata."""
        # HTML formatter should use HTML formatter's metadata format
        html_result = self.html_formatter.format_metadata(TEST_METADATA)
        assert "<h2>Codebase Metadata</h2>" in html_result
        assert "<table>" in html_result
        
        # Terminal formatter should use plain text formatter's metadata format
        terminal_result = self.terminal_formatter.format_metadata(TEST_METADATA)
        assert "# Codebase Metadata" in terminal_result
    
    def test_format_error(self):
        """Test formatting error message."""
        # HTML formatter should use HTML formatter's error format
        html_result = self.html_formatter.format_error(TEST_ERROR)
        assert "<div class='error-message'" in html_result
        
        # Terminal formatter should use plain text formatter's error format
        terminal_result = self.terminal_formatter.format_error(TEST_ERROR)
        assert "# " + TEST_ERROR in terminal_result
    
    def test_format_skipped_files(self):
        """Test formatting skipped files."""
        # HTML formatter should use HTML formatter's skipped files format
        html_result = self.html_formatter.format_skipped_files(TEST_SKIPPED_FILES)
        assert "<h2>Files skipped due to size limit</h2>" in html_result
        assert "<table>" in html_result
        
        # Terminal formatter should use plain text formatter's skipped files format
        terminal_result = self.terminal_formatter.format_skipped_files(TEST_SKIPPED_FILES)
        assert "# Files skipped due to size limit" in terminal_result
    
    def test_format_skipped_files_empty(self):
        """Test formatting empty skipped files list."""
        html_result = self.html_formatter.format_skipped_files([])
        terminal_result = self.terminal_formatter.format_skipped_files([])
        assert html_result == ""
        assert terminal_result == ""
    
    def test_get_full_html(self):
        """Test getting full HTML document."""
        content = "<p>Test content</p>"
        title = "Test Title"
        
        # HTML formatter should return full HTML
        html_result = self.html_formatter.get_full_html(content, title)
        assert "<!DOCTYPE html>" in html_result
        assert title in html_result
        assert content in html_result
        
        # Terminal formatter should just return the content
        terminal_result = self.terminal_formatter.get_full_html(content, title)
        assert terminal_result == content


def test_custom_template_formatter(tmp_path):
    """Test the CustomTemplateFormatter with a simple template."""
    # Create a template file
    template_file = tmp_path / "template.txt"
    template_content = """
Title: ${TITLE}

Directory Tree:
${DIRECTORY_TREE}

Files:
${FILES}

Metadata:
${METADATA}
"""
    template_file.write_text(template_content)

    # Sample data
    directory_tree = """root/
  ├── file1.py
  └── file2.py"""
    files_content = {"file1.py": "def foo(): pass", "file2.py": "def bar(): pass"}
    metadata = {"files": 2, "lines": 10}
    skipped_files = []

    # Test the formatter
    formatter = CustomTemplateFormatter(str(template_file), "plain")
    result = formatter.render_template(directory_tree, files_content, metadata, skipped_files, "Test Title")

    # Verify placeholders are replaced
    assert "Title: Test Title" in result
    assert directory_tree in result
    assert "file1.py" in result
    assert "file2.py" in result
    assert "# Codebase Metadata" in result
    assert "# Files: 2" in result
    assert "# Lines: 10" in result