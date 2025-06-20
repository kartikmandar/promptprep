import os
import subprocess
import sys
import tempfile


def run_script(args, cwd):
    """Runs our CLI script and returns its output for testing."""
    # Get the path to the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Get the path to the CLI script
    cli_script = os.path.join(project_root, "promptprep", "cli.py")

    # Set up environment with PYTHONPATH to ensure imports work
    env = os.environ.copy()
    env["PYTHONPATH"] = project_root

    cmd = [sys.executable, cli_script] + args

    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
    return result


def test_default_output():
    """Makes sure we can create an output file using default settings."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_script(["-d", tmpdir], cwd=tmpdir)
        assert result.returncode == 0
        output_file = os.path.join(tmpdir, "full_code.txt")
        assert os.path.exists(output_file)


def test_specified_directory():
    """Verifies we can process files from any directory we choose."""
    with tempfile.TemporaryDirectory() as src_dir:
        dummy_file = os.path.join(src_dir, "dummy.py")
        with open(dummy_file, "w", encoding="utf-8") as f:
            f.write("print('hello')")

        with tempfile.TemporaryDirectory() as work_dir:
            custom_output = "test_output.txt"
            result = run_script(["-d", src_dir, "-o", custom_output], cwd=work_dir)
            assert result.returncode == 0
            output_file = os.path.join(work_dir, custom_output)
            assert os.path.exists(output_file)


def test_include_files():
    """Checks if we only process the specific files we ask for."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = os.path.join(tmpdir, "include_me.py")
        file2 = os.path.join(tmpdir, "ignore_me.py")
        with open(file1, "w", encoding="utf-8") as f:
            f.write("print('include me')")
        with open(file2, "w", encoding="utf-8") as f:
            f.write("print('ignore me')")

        result = run_script(["-d", tmpdir, "-i", "include_me.py"], cwd=tmpdir)
        assert result.returncode == 0
        output_file = os.path.join(tmpdir, "full_code.txt")
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert "include_me.py" in content
        assert "ignore_me.py" not in content


def test_extensions():
    """Verifies we only process files with the extensions we want."""
    with tempfile.TemporaryDirectory() as tmpdir:
        py_file = os.path.join(tmpdir, "dummy.py")
        txt_file = os.path.join(tmpdir, "dummy.txt")
        with open(py_file, "w", encoding="utf-8") as f:
            f.write("print('hello')")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("Text content")

        result = run_script(["-d", tmpdir, "-x", ".py"], cwd=tmpdir)
        assert result.returncode == 0
        output_file = os.path.join(tmpdir, "full_code.txt")
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert "dummy.py" in content
        assert "dummy.txt" not in content


def test_exclude_dirs():
    """Makes sure we properly skip directories we want to exclude."""
    with tempfile.TemporaryDirectory() as tmpdir:
        exclude_dir = os.path.join(tmpdir, "exclude_this")
        os.mkdir(exclude_dir)
        file_in_exclude = os.path.join(exclude_dir, "dummy.py")
        with open(file_in_exclude, "w", encoding="utf-8") as f:
            f.write("print('excluded')")

        result = run_script(["-d", tmpdir, "-e", "exclude_this"], cwd=tmpdir)
        assert result.returncode == 0
        output_file = os.path.join(tmpdir, "full_code.txt")
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert "exclude_this/ [EXCLUDED]" in content
        assert "dummy.py" not in content
