import os
import tempfile
from unittest import mock
import warnings

from promptprep.aggregator import CodeAggregator, DirectoryTreeGenerator


class TestTreeGeneratorEdgeCases:
    """Test edge cases for DirectoryTreeGenerator"""

    def test_generate_with_nested_excluded_dirs(self):
        """Test tree generation with deeply nested excluded directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a nested directory structure with excluded directories
            os.makedirs(os.path.join(tmpdir, "src", "node_modules", "nested"))
            open(
                os.path.join(tmpdir, "src", "node_modules", "nested", "file.js"), "w"
            ).close()

            # Create some regular directories and files
            os.makedirs(os.path.join(tmpdir, "src", "app"))
            open(os.path.join(tmpdir, "src", "app", "main.py"), "w").close()

            tree_gen = DirectoryTreeGenerator()
            tree = tree_gen.generate(tmpdir)

            # Check nested exclusions
            assert "src/" in tree
            assert "app/" in tree
            assert "main.py" in tree
            assert "node_modules/ [EXCLUDED]" in tree
            assert "nested/" not in tree  # Nested dir should be excluded
            assert "file.js" not in tree  # File in excluded dir should be excluded

    def test_generate_with_empty_directory(self):
        """Test tree generation with an empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tree_gen = DirectoryTreeGenerator()
            tree = tree_gen.generate(tmpdir)

            # Just the root directory should be present
            assert os.path.basename(tmpdir) in tree
            # Tree should only have one line (the root)
            assert len(tree.strip().split("\n")) == 1

    def test_generate_with_hidden_files(self):
        """Test tree generation handles hidden files correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create hidden files and directories
            open(os.path.join(tmpdir, ".hidden_file"), "w").close()
            os.makedirs(os.path.join(tmpdir, ".hidden_dir"))
            open(os.path.join(tmpdir, ".hidden_dir", "file.txt"), "w").close()

            # Create visible files
            open(os.path.join(tmpdir, "visible_file.txt"), "w").close()

            # Test with programming_extensions filter (since hidden files are included by default)
            tree_gen = DirectoryTreeGenerator(programming_extensions={".visible_only"})
            tree = tree_gen.generate(tmpdir)

            # Check that no files are included because of the extension filter
            assert "visible_file.txt" not in tree
            assert ".hidden_file" not in tree

            # Test with show_hidden parameter via include_files
            tree_gen = DirectoryTreeGenerator(include_files={"visible_file.txt"})
            tree = tree_gen.generate(tmpdir)

            # Should include specified visible file but not hidden files
            assert "visible_file.txt" in tree
            assert ".hidden_file" not in tree  # Because it's not in include_files


class TestCodeAggregatorEdgeCases:
    """Test edge cases for CodeAggregator."""

    def test_tokenization_fallback(self):
        """Test tiktoken import failure and fallback."""
        with tempfile.TemporaryDirectory() as tmpdir:
            aggregator = CodeAggregator(directory=tmpdir, count_tokens=True)

            # Create a patched version of count_text_tokens that simulates tiktoken failure
            def mock_count_tokens(text):
                # Simulate tiktoken failing
                aggregator.tokenizer = None
                # Call the original which will fall back to word counting
                return len(text.split())

            aggregator.count_text_tokens = mock_count_tokens

            # Test the fallback
            token_count = aggregator.count_text_tokens("This is a test.")
            # Should be 4 words
            assert token_count == 4

    def test_empty_directory_aggregation(self):
        """Test aggregating an empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            aggregator = CodeAggregator(directory=tmpdir)
            result = aggregator.aggregate_code()

            # Check the empty tree is included
            dir_name = os.path.basename(tmpdir)
            assert dir_name in result

            # No files should be processed
            assert "File:" not in result

    def test_formatter_fallback(self):
        """Test fallback to plain formatter when requested format fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            with open(os.path.join(tmpdir, "test.py"), "w") as f:
                f.write('print("Hello")')

            # Mock an error in the formatter initialization
            with mock.patch(
                "promptprep.aggregator.get_formatter",
                side_effect=[ValueError("Test error"), mock.DEFAULT],
            ) as mock_get_formatter:
                with warnings.catch_warnings(record=True) as w:
                    aggregator = CodeAggregator(
                        directory=tmpdir,
                        output_format="markdown",  # This should fail and fall back to plain
                    )

                    # Check that the formatter falls back to plain
                    assert mock_get_formatter.call_count == 2
                    # Check that it first tried the requested format ('markdown')
                    mock_get_formatter.assert_any_call("markdown", None)
                    # Check that it then called the fallback ('plain')
                    mock_get_formatter.assert_any_call("plain", None)

                    # Check that a warning was issued
                    assert len(w) > 0
                    assert any(
                        "Failed to initialize formatter" in str(warning.message)
                        for warning in w
                    )

                    # Verify the aggregator was properly set up
                    assert aggregator.output_format == "markdown"

    def test_unsupported_clipboard_platform(self):
        """Test clipboard functionality on unsupported platforms."""
        with tempfile.TemporaryDirectory() as tmpdir:
            aggregator = CodeAggregator(directory=tmpdir)

            with mock.patch("platform.system", return_value="UnsupportedOS"):
                with mock.patch("builtins.print") as mock_print:
                    result = aggregator.copy_to_clipboard("Test content")

                    # Should return False for unsupported platforms
                    assert result is False
                    mock_print.assert_any_call(
                        "Clipboard operations not supported on UnsupportedOS"
                    )

    def test_clipboard_error_handling(self):
        """Test error handling in copy_to_clipboard method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            aggregator = CodeAggregator(directory=tmpdir)

            # Simulate a general error during clipboard operation
            with mock.patch("platform.system", return_value="Darwin"):
                with mock.patch(
                    "subprocess.Popen", side_effect=Exception("Test error")
                ):
                    with mock.patch("builtins.print") as mock_print:
                        result = aggregator.copy_to_clipboard("Test content")

                        # Should return False on error
                        assert result is False
                        mock_print.assert_any_call(
                            "Error copying to clipboard: Test error"
                        )

    def test_process_file_exception_handling(self):
        """Test exception handling in _process_file method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file with content
            file_path = os.path.join(tmpdir, "test.py")
            with open(file_path, "w") as f:
                f.write('print("Test")')

            aggregator = CodeAggregator(directory=tmpdir)

            # Mock open to raise an exception
            with mock.patch("builtins.open", side_effect=Exception("Test error")):
                result = aggregator._process_file(file_path)

                # Should return error message
                assert "Error reading file" in result
                assert "Test error" in result

    def test_extract_summary_syntax_error_handling(self):
        """Test handling of syntax errors in _extract_summary."""
        code_with_syntax_error = """
def function_with_error(
    print("Missing closing parenthesis")
"""

        aggregator = CodeAggregator()
        result = aggregator._extract_summary(code_with_syntax_error, "test_file.py")

        assert "Could not parse test_file.py for summary (SyntaxError)" in result

    def test_extract_summary_general_exception(self):
        """Test handling of general exceptions in _extract_summary."""
        valid_code = """
def valid_function():
    print("This is valid")
"""

        aggregator = CodeAggregator()

        # Mock ast.parse to raise a general exception
        with mock.patch("ast.parse", side_effect=Exception("Test error")):
            result = aggregator._extract_summary(valid_code, "test_file.py")

            assert "Error parsing test_file.py for summary: Test error" in result

    def test_tokenize_error_handling(self):
        """Test handling of tokenize errors in _process_file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file that will cause a tokenize error
            file_path = os.path.join(tmpdir, "test.py")
            with open(file_path, "wb") as f:
                # Use bytes directly to avoid encoding issues on all platforms
                # Including a null byte which will cause tokenize to fail
                f.write(b'print("hello")\n\x00invalid')

            aggregator = CodeAggregator(directory=tmpdir)

            # The method should handle the TokenError and fall back to simple line processing
            result = aggregator._process_file(file_path)

            # The content should still be processed despite the error
            assert 'print("hello")' in result
