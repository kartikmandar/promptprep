import os
import subprocess
import platform
from typing import Optional, Set


class DirectoryTreeGenerator:
    def __init__(
        self, 
        exclude_dirs: Optional[Set[str]] = None, 
        include_files: Optional[Set[str]] = None, 
        exclude_files: Optional[Set[str]] = None,
        programming_extensions: Optional[Set[str]] = None
    ):
        # Default directories to exclude
        self.exclude_dirs = exclude_dirs or {
            "venv", "node_modules", "__pycache__", ".git", "dist", "build", "temp", "old_files", "flask_session"
        }
        self.include_files = include_files or set()
        self.exclude_files = exclude_files or set()
        self.programming_extensions = programming_extensions

    def generate(self, start_path: str) -> str:
        """Generates an ASCII representation of the directory tree starting from start_path."""
        if not os.path.exists(start_path):
            return f"Directory not found: {start_path}\n"
        
        tree = ""
        for root, dirs, files in os.walk(start_path):
            rel_path = os.path.relpath(root, start_path)
            if rel_path == ".":
                rel_path = ""
            path_parts = rel_path.split(os.sep) if rel_path else []
            level = len(path_parts)
            indent = "│   " * level + ("├── " if level > 0 else "")
            current_dir = os.path.basename(root) if rel_path else os.path.basename(start_path.rstrip(os.sep)) or start_path
            if current_dir in self.exclude_dirs:
                tree += f"{indent}{current_dir}/ [EXCLUDED]\n"
                dirs[:] = []  # Do not traverse further in this directory.
                continue
            tree += f"{indent}{current_dir}/\n"
            
            # Filter files based on include_files, exclude_files, and programming_extensions
            filtered_files = files
            if self.include_files or self.exclude_files or self.programming_extensions:
                filtered_files = []
                for f in files:
                    file_path = os.path.join(rel_path, f) if rel_path else f
                    if f in self.exclude_files:
                        continue
                    if self.include_files and file_path not in self.include_files:
                        continue
                    if self.programming_extensions:
                        _, ext = os.path.splitext(f)
                        if ext.lower() not in self.programming_extensions:
                            continue
                    filtered_files.append(f)
                
            for f in filtered_files:
                tree += f"{'│   ' * (level + 1)}├── {f}\n"
        return tree


class CodeAggregator:
    DEFAULT_PROGRAMMING_EXTENSIONS = {
        # General Programming Languages
        ".py", ".java", ".c", ".cpp", ".h", ".hpp", ".cs", ".vb", ".r",
        ".rb", ".go", ".php", ".swift", ".kt", ".rs", ".scala", ".pl", ".lua",
        # Web Development
        ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".scss", ".less", ".sass",
        # Shell & Automation
        ".sh", ".zsh", ".fish", ".ps1", ".bat", ".cmd",
        # Database & Query Languages
        ".sql", ".psql", ".db", ".sqlite",
        # Markup & Config Files
        ".xml", ".json", ".toml", ".ini", ".yml", ".yaml", ".md", ".rst",
        # Build & Make Systems
        ".Makefile", ".gradle", ".cmake", ".ninja",
        # Other
        ".pqm", ".pq"
    }

    DEFAULT_EXCLUDE_FILES = {"full_code.txt"}
    DEFAULT_EXCLUDE_DIRS = {
        "venv", "node_modules", "__pycache__", ".git", "dist", "build", "temp", "old_files", "flask_session"
    }

    def __init__(
        self,
        directory: Optional[str] = None,
        output_file: str = "full_code.txt",
        include_files: Optional[Set[str]] = None,
        programming_extensions: Optional[Set[str]] = None,
        exclude_dirs: Optional[Set[str]] = None,
        exclude_files: Optional[Set[str]] = None,
    ):
        self.directory = directory or os.getcwd()
        self.output_file = output_file
        self.include_files = include_files or set()
        self.programming_extensions = programming_extensions or self.DEFAULT_PROGRAMMING_EXTENSIONS
        self.exclude_dirs = exclude_dirs or self.DEFAULT_EXCLUDE_DIRS
        self.exclude_files = exclude_files or self.DEFAULT_EXCLUDE_FILES
        self.tree_generator = DirectoryTreeGenerator(self.exclude_dirs, self.include_files, self.exclude_files, self.programming_extensions)

    def is_programming_file(self, filename: str) -> bool:
        _, ext = os.path.splitext(filename)
        return ext.lower() in self.programming_extensions

    def should_exclude(self, path: str) -> bool:
        normalized_path = os.path.normpath(path)
        parts = normalized_path.split(os.sep)
        for part in parts[:-1]:
            if part in self.exclude_dirs:
                return True
        if parts[-1] in self.exclude_files:
            return True
        return False

    def should_include(self, file_path: str) -> bool:
        if not self.include_files:
            return True
        rel_file_path = os.path.relpath(file_path, self.directory)
        return rel_file_path in self.include_files

    def aggregate_code(self) -> str:
        """Aggregates the directory tree and the content of programming-related files."""
        tree = self.tree_generator.generate(self.directory)
        aggregated = f"Directory Tree:\n{tree}\n\n"
        
        # If directory doesn't exist, just return the tree (which will have the error message)
        if "Directory not found" in tree:  # pragma: no cover
            return aggregated  # pragma: no cover
            
        for root, dirs, files in os.walk(self.directory):
            rel_path = os.path.relpath(root, self.directory)
            if rel_path == ".":
                rel_path = ""
            # If any parent directory is excluded, skip this branch.
            if any(part in self.exclude_dirs for part in (rel_path.split(os.sep) if rel_path else [])):
                dirs[:] = []
                continue
            current_dir = os.path.basename(root) if rel_path else os.path.basename(self.directory.rstrip(os.sep)) or self.directory
            if current_dir in self.exclude_dirs:
                dirs[:] = [] # pragma: no cover
                continue # pragma: no cover
            for file in files:
                if not self.is_programming_file(file):
                    continue
                file_path = os.path.join(root, file)
                rel_file_path = os.path.relpath(file_path, self.directory)
                if self.should_exclude(rel_file_path) or not self.should_include(file_path):
                    continue
                header = (
                    f"\n\n# ======================\n"
                    f"# File: {rel_file_path}\n"
                    f"# ======================\n\n"
                )
                aggregated += header
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        aggregated += f.read()
                except Exception as e:
                    aggregated += f"\n# Error reading file {rel_file_path}: {e}\n"
        return aggregated

    def write_to_file(self, content: Optional[str] = None, filename: Optional[str] = None) -> None:
        """Writes the aggregated content to a file."""
        content = content or self.aggregate_code()
        filename = filename or self.output_file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    def copy_to_clipboard(self, content: Optional[str] = None) -> bool:
        """Copies the aggregated content to the clipboard across different platforms."""
        content = content or self.aggregate_code()
        try:
            system = platform.system()
            
            if system == 'Darwin':  # macOS
                process = subprocess.Popen("pbcopy", env={"LANG": "en_US.UTF-8"}, stdin=subprocess.PIPE)
                process.communicate(content.encode("utf-8"))
                return True
            elif system == 'Windows':
                process = subprocess.Popen("clip", stdin=subprocess.PIPE)
                process.communicate(content.encode("utf-8"))
                return True
            elif system == 'Linux':
                # Try different clipboard commands available on Linux
                for cmd in ['xclip -selection clipboard', 'xsel -ib']:
                    try:
                        process = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE)
                        process.communicate(content.encode("utf-8"))
                        return True
                    except FileNotFoundError:
                        continue
                print("Could not find clipboard command. Please install xclip or xsel.")
                return False
            else:
                print(f"Clipboard operations not supported on {system}")
                return False
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
            return False
