import os
import subprocess
import sys
import tempfile
import pytest
from unittest import mock
import platform

from PromptPrep.aggregator import CodeAggregator, DirectoryTreeGenerator

# Helper function to run CLI script
def run_script(args, cwd):
    cmd = [sys.executable, os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "PromptPrep", "cli.py")] + args
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result

def test_default_output():
    """Test default output file creation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        run_script(["-d", tmpdir], cwd=tmpdir)
        output_file = os.path.join(tmpdir, "full_code.txt")
        assert os.path.exists(output_file)


def test_specified_directory():
    """Test with specified directory."""
    with tempfile.TemporaryDirectory() as src_dir:
        dummy_file = os.path.join(src_dir, "dummy.py")
        with open(dummy_file, "w", encoding="utf-8") as f:
            f.write("print('hello')")
        
        with tempfile.TemporaryDirectory() as work_dir:
            custom_output = "test_output.txt"
            run_script(["-d", src_dir, "-o", custom_output], cwd=work_dir)
            output_file = os.path.join(work_dir, custom_output)
            assert os.path.exists(output_file)


def test_include_files():
    """Test include_files parameter."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = os.path.join(tmpdir, "include_me.py")
        file2 = os.path.join(tmpdir, "ignore_me.py")
        with open(file1, "w", encoding="utf-8") as f:
            f.write("print('include me')")
        with open(file2, "w", encoding="utf-8") as f:
            f.write("print('ignore me')")
        
        run_script(["-d", tmpdir, "-i", "include_me.py"], cwd=tmpdir)
        output_file = os.path.join(tmpdir, "full_code.txt")
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert "include_me.py" in content
        assert "ignore_me.py" not in content


def test_extensions():
    """Test extensions parameter."""
    with tempfile.TemporaryDirectory() as tmpdir:
        py_file = os.path.join(tmpdir, "dummy.py")
        txt_file = os.path.join(tmpdir, "dummy.txt")
        with open(py_file, "w", encoding="utf-8") as f:
            f.write("print('hello')")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("Text content")
        
        run_script(["-d", tmpdir, "-x", ".py"], cwd=tmpdir)
        output_file = os.path.join(tmpdir, "full_code.txt")
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert "dummy.py" in content
        assert "dummy.txt" not in content


def test_exclude_dirs():
    """Test exclude_dirs parameter."""
    with tempfile.TemporaryDirectory() as tmpdir:
        exclude_dir = os.path.join(tmpdir, "exclude_this")
        os.mkdir(exclude_dir)
        file_in_exclude = os.path.join(exclude_dir, "dummy.py")
        with open(file_in_exclude, "w", encoding="utf-8") as f:
            f.write("print('excluded')")
        
        run_script(["-d", tmpdir, "-e", "exclude_this"], cwd=tmpdir)
        output_file = os.path.join(tmpdir, "full_code.txt")
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert "exclude_this/ [EXCLUDED]" in content
        assert "dummy.py" not in content

