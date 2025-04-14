import os
import subprocess
import platform
from typing import Optional, Set, Dict, Any, List, Tuple
from tqdm import tqdm
import ast
from pathlib import Path
import tokenize
import io
import warnings
import tiktoken
import difflib
from .formatters import get_formatter, BaseFormatter, CustomTemplateFormatter



class DirectoryTreeGenerator:
    def __init__(
        self, 
        exclude_dirs: Optional[Set[str]] = None, 
        include_files: Optional[Set[str]] = None, 
        exclude_files: Optional[Set[str]] = None,
        programming_extensions: Optional[Set[str]] = None
    ):
        self.exclude_dirs = exclude_dirs or {
            "venv", "node_modules", "__pycache__", ".git", "dist", "build", "temp", "old_files", "flask_session"
        }
        self.include_files = include_files or set()
        self.exclude_files = exclude_files or set()
        self.programming_extensions = programming_extensions

    def generate(self, start_path: str) -> str:
        """Creates an ASCII representation of the directory structure starting from the given path."""
        if not os.path.exists(start_path):
            raise FileNotFoundError(f"Directory not found: {start_path}")
        
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
                dirs[:] = []  # Skip this directory's contents
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
    DEFAULT_MAX_FILE_SIZE_MB = 100.0
    DEFAULT_TOKEN_MODEL = "cl100k_base"

    def __init__(
        self,
        directory: Optional[str] = None,
        output_file: str = "full_code.txt",
        include_files: Optional[Set[str]] = None,
        programming_extensions: Optional[Set[str]] = None,
        exclude_dirs: Optional[Set[str]] = None,
        exclude_files: Optional[Set[str]] = None,
        max_file_size_mb: Optional[float] = None,
        summary_mode: bool = False,
        include_comments: bool = True,
        collect_metadata: bool = False,
        count_tokens: bool = False,
        token_model: str = DEFAULT_TOKEN_MODEL,
        output_format: str = "plain",
        line_numbers: bool = False,
        template_file: Optional[str] = None,
        incremental: bool = False,
        last_run_timestamp: Optional[float] = None
    ):
        self.directory = directory or os.getcwd()
        self.output_file = output_file
        self.include_files = include_files or set()
        self.programming_extensions = programming_extensions or self.DEFAULT_PROGRAMMING_EXTENSIONS
        self.exclude_dirs = exclude_dirs or self.DEFAULT_EXCLUDE_DIRS
        self.exclude_files = exclude_files or self.DEFAULT_EXCLUDE_FILES
        self.max_file_size_mb = max_file_size_mb or self.DEFAULT_MAX_FILE_SIZE_MB
        self.tree_generator = DirectoryTreeGenerator(self.exclude_dirs, self.include_files, self.exclude_files, self.programming_extensions)
        self.summary_mode = summary_mode
        self.include_comments = include_comments
        self.include_metadata = collect_metadata
        self.count_tokens = count_tokens
        self.token_model = token_model
        self.output_format = output_format
        self.line_numbers = line_numbers
        self.template_file = template_file
        self.incremental = incremental
        self.last_run_timestamp = last_run_timestamp
        self.file_mod_times: Dict[str, float] = {}
        self.metadata = {
            'total_files': 0,
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
        }
        
        # Initialize tokenizer if token counting is enabled
        self.tokenizer = None
        if self.count_tokens:
            try:
                self.tokenizer = tiktoken.get_encoding(self.token_model)
            except Exception as e:
                warnings.warn(f"Failed to load tokenizer model '{self.token_model}': {e}. Token counting will be unavailable.")

        # Initialize formatter
        try:
            self.formatter = get_formatter(self.output_format, self.template_file)
        except (ValueError, ImportError) as e:
            warnings.warn(f"Failed to initialize formatter for format '{self.output_format}': {e}. Falling back to plain text.")
            self.formatter = get_formatter("plain", None)

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

    def is_file_size_within_limit(self, file_path: str) -> bool:
        """Check if the file size is within our configured limit."""
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / (1024 * 1024)  # Convert to MB
        return file_size_mb <= self.max_file_size_mb

    def count_text_tokens(self, text: str) -> int:
        """Count the number of tokens in a text string using our tokenizer."""
        if not self.tokenizer:
            self.tokenizer = tiktoken.get_encoding(self.token_model)
        
        try:
            tokens = self.tokenizer.encode(text)
            return len(tokens)
        except Exception as e:
            warnings.warn(f"Error counting tokens: {e}. Returning estimated count.")
            # Fallback to a rough approximation when tokenizer fails
            return len(text.split())

    def _get_file_mod_time(self, file_path: str) -> float:
        """Get the last modified time of a file."""
        return os.path.getmtime(file_path)

    def _is_file_changed(self, file_path: str) -> bool:
        """Check if a file has been modified since our last run."""
        if not self.incremental or not self.last_run_timestamp:
            return True
        mod_time = self._get_file_mod_time(file_path)
        return mod_time > self.last_run_timestamp

    def aggregate_code(self) -> str:
        """Brings together the directory tree and content of programming files into a single document."""
        is_custom_format = isinstance(self.formatter, CustomTemplateFormatter)
        tree = self.tree_generator.generate(self.directory)
        
        if "Directory not found" in tree:
            error_message = f"Directory not found: {self.directory}"
            return self.formatter.format_error(error_message)

        # Find files to process
        files_to_process = []
        skipped_files_data = []
        for root, dirs, files in os.walk(self.directory):
            rel_path_for_exclusion_check = os.path.relpath(root, self.directory)
            if rel_path_for_exclusion_check == ".":
                rel_path_for_exclusion_check = ""
            
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs and 
                       not any(part in self.exclude_dirs for part in os.path.join(rel_path_for_exclusion_check, d).split(os.sep))]

            current_dir = os.path.basename(root)
            if current_dir in self.exclude_dirs:
                 continue

            for file in files:
                if not self.is_programming_file(file):
                    continue
                file_path = os.path.join(root, file)
                rel_file_path = os.path.relpath(file_path, self.directory)
                if self.should_exclude(rel_file_path) or not self.should_include(file_path):
                    continue

                if not self.is_file_size_within_limit(file_path):
                    skipped_files_data.append((rel_file_path, os.path.getsize(file_path) / (1024 * 1024)))
                    continue

                if self._is_file_changed(file_path):
                    files_to_process.append(file_path)

       # Custom format processing
        if is_custom_format:
            aggregated_data = {
                "directory_tree": tree,
                "files_content": {},
                "metadata": {},
                "skipped_files": skipped_files_data,
                "title": f"Code Aggregation - {os.path.basename(self.directory)}"
            }
            if self.include_metadata or self.count_tokens:
                 aggregated_data["metadata"] = self.collect_metadata()
                 if self.count_tokens:
                     aggregated_data["metadata"]["token_model"] = self.token_model

            # Process files for the template
            for file_path in tqdm(files_to_process, desc="Aggregating files", unit="file", leave=False):
                rel_file_path = os.path.relpath(file_path, self.directory)
                try:
                    with open(file_path, "r", encoding="utf-8", errors='ignore') as f:
                        content = f.read()
                        if not self.include_comments:
                            content = "\n".join(line for line in content.splitlines() if not line.strip().startswith('#'))
                        if self.summary_mode:
                            content = self._extract_summary(content, file_path)

                        if self.line_numbers:
                            lines = content.splitlines()
                            padding = len(str(len(lines)))
                            content = "\n".join(
                                f"{str(i).rjust(padding)} | {line}"
                                for i, line in enumerate(lines, 1)
                            )

                        aggregated_data["files_content"][rel_file_path] = content
                except Exception as e:
                     aggregated_data["files_content"][rel_file_path] = f"# Error reading file {rel_file_path}: {e}\n"

            # Render the custom template
            return self.formatter.render_template(
                aggregated_data["directory_tree"],
                aggregated_data["files_content"],
                aggregated_data["metadata"],
                aggregated_data["skipped_files"],
                aggregated_data["title"]
            )

        # Standard format processing
        else:
            aggregated = ""
            total_tokens = 0
            metadata_dict = {}
            if self.include_metadata or self.count_tokens:
                metadata_dict = self.collect_metadata()
                if self.count_tokens:
                    metadata_dict["token_model"] = self.token_model
                    metadata_dict["total_tokens"] = "[placeholder]"

                if self.include_metadata:
                    metadata_section = self.formatter.format_metadata(metadata_dict)
                    aggregated += metadata_section + "\n\n"
                    if self.count_tokens:
                        metadata_tokens = self.count_text_tokens(metadata_section)
                        total_tokens += metadata_tokens

            tree_section = self.formatter.format_directory_tree(tree)
            aggregated += tree_section
            if self.count_tokens:
                tree_tokens = self.count_text_tokens(tree_section)
                total_tokens += tree_tokens

            for file_path in tqdm(files_to_process, desc="Aggregating files", unit="file", leave=False):
                rel_file_path = os.path.relpath(file_path, self.directory)
                header = self.formatter.format_file_header(rel_file_path)
                aggregated += header
                if self.count_tokens:
                    total_tokens += self.count_text_tokens(header)

                try:
                    with open(file_path, "r", encoding="utf-8", errors='ignore') as f:
                        content = f.read()

                        if not self.include_comments:
                            processed_lines = []
                            for line in content.splitlines():
                                code_part = line.split('#', 1)[0]
                                if code_part.strip() or not line.strip():
                                    processed_lines.append(code_part.rstrip())
                            content = "\n".join(processed_lines)

                        if self.summary_mode:
                            content = self._extract_summary(content, file_path)

                        formatted_content = self.formatter.format_code_content(content, file_path)

                        if self.line_numbers:
                            lines = formatted_content.splitlines()
                            padding = len(str(len(lines)))
                            formatted_content = "\n".join(
                                f"{str(i).rjust(padding)} | {line}"
                                for i, line in enumerate(lines, 1)
                            )

                        if self.count_tokens:
                            file_tokens = self.count_text_tokens(formatted_content)
                            total_tokens += file_tokens

                        aggregated += formatted_content
                except Exception as e:
                    error_msg = f"Error reading file {rel_file_path}: {e}"
                    formatted_error = self.formatter.format_error(error_msg)
                    aggregated += formatted_error
                    if self.count_tokens:
                        total_tokens += self.count_text_tokens(formatted_error)

            if skipped_files_data:
                skipped_section = self.formatter.format_skipped_files(
                    [(path, size_mb) for path, size_mb in skipped_files_data]
                )
                aggregated += skipped_section
                if self.count_tokens:
                    total_tokens += self.count_text_tokens(skipped_section)

            if self.count_tokens and "[placeholder]" in aggregated:
                formatted_token_count = f"{total_tokens:,}"
                aggregated = aggregated.replace("[placeholder]", formatted_token_count)

            if hasattr(self.formatter, 'get_full_html'):
                title = f"Code Aggregation - {os.path.basename(self.directory)}"
                aggregated = self.formatter.get_full_html(aggregated, title)

            return aggregated

    def write_to_file(self, content: Optional[str] = None, filename: Optional[str] = None) -> None:
        """Writes the aggregated content to a file with appropriate extension based on format."""
        content = content or self.aggregate_code()
        filename = filename or self.output_file
        
        # Add HTML extension if needed
        if self.output_format in ["html", "highlighted"] and not filename.lower().endswith(".html"):
            root, _ = os.path.splitext(filename)
            filename = f"{root}.html"
        
        # Add Markdown extension if needed
        if self.output_format == "markdown" and not filename.lower().endswith((".md", ".markdown")):
            root, _ = os.path.splitext(filename)
            filename = f"{root}.md"
            
        try:
            # Create the directory if needed
            output_dir = os.path.dirname(filename)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
                
            # Update the output_file attribute to match the actual filename used
            self.output_file = filename
        except IOError as e:
            raise IOError(f"Error writing to file {filename}: {e}")

    def copy_to_clipboard(self, content: Optional[str] = None) -> bool:
        """Copies the content to clipboard, with platform-specific handling."""
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
                # Try available clipboard commands 
                for cmd in ['xclip -selection clipboard', 'xsel -ib']:
                    try:
                        process = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE)
                        process.communicate(content.encode("utf-8"))
                        return True
                    except FileNotFoundError:
                        print("Could not find clipboard command. Please install xclip or xsel.")
                        return False
                    except Exception as e:
                        print(f"Error executing clipboard command: {cmd}: {e}")
                        continue
                print("Could not find clipboard command. Please install xclip or xsel.")
                return False
            else:
                print(f"Clipboard operations not supported on {system}")
                return False
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
            return False

    def collect_metadata(self) -> dict:
        """Gathers stats about the codebase like lines of code and comment ratio."""
        total_lines = 0
        comment_lines = 0
        code_files = 0

        for root, _, files in os.walk(self.directory):
            for file in files:
                if not self.is_programming_file(file):
                    continue
                file_path = os.path.join(root, file)
                rel_file_path = os.path.relpath(file_path, self.directory)
                if self.should_exclude(rel_file_path) or not self.should_include(file_path):
                    continue

                code_files += 1
                try:
                    with open(file_path, "r", encoding="utf-8", errors='ignore') as f:
                        lines = f.readlines()
                        total_lines += len(lines)
                        comment_lines += sum(1 for line in lines if line.strip().startswith("#"))
                except Exception:
                    pass

        comment_ratio = (comment_lines / total_lines) if total_lines else 0
        return {
            "total_lines": total_lines,
            "comment_lines": comment_lines,
            "comment_ratio": comment_ratio,
            "code_files": code_files,
        }

    def _process_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.metadata['total_files'] += 1
            lines = content.splitlines()
            file_lines = len(lines)
            self.metadata['total_lines'] += file_lines

            if self.summary_mode:
                return self._extract_summary(content, file_path)
            else:
                processed_lines = []
                file_code_lines = 0
                file_comment_lines = 0
                file_blank_lines = 0

                try:
                    # Use tokenize for better comment/code detection
                    g = tokenize.tokenize(io.BytesIO(content.encode('utf-8')).readline)
                    for token_info in g:
                        if token_info.type == tokenize.NL:
                            continue
                        elif token_info.type == tokenize.NEWLINE:
                             processed_lines.append("")
                             file_blank_lines += 1
                        elif token_info.type == tokenize.COMMENT:
                            if self.include_comments:
                                processed_lines.append(token_info.string)
                            file_comment_lines += 1
                        elif token_info.type == tokenize.ENDMARKER:
                            continue
                        else:
                             line_num = token_info.start[0] -1
                             if line_num < len(lines):
                                 current_line = lines[line_num]
                                 if not processed_lines or processed_lines[-1] != current_line:
                                     processed_lines.append(current_line)
                                     file_code_lines += 1

                except tokenize.TokenError:
                     # Fallback for non-Python files
                     for line in lines:
                         stripped_line = line.strip()
                         is_comment = stripped_line.startswith('#')
                         is_blank = not stripped_line

                         if is_blank:
                             file_blank_lines += 1
                             processed_lines.append(line)
                         elif is_comment:
                             file_comment_lines += 1
                             if self.include_comments:
                                 processed_lines.append(line)
                         else:
                             file_code_lines += 1
                             processed_lines.append(line)


                self.metadata['code_lines'] += file_code_lines
                self.metadata['comment_lines'] += file_comment_lines
                self.metadata['blank_lines'] += file_blank_lines

                return "\n".join(processed_lines)

        except Exception as e:
            return f"\n# Error reading file {file_path}: {e}\n"

    def _extract_summary(self, content, file_path):
        """Extracts class/function definitions and their docstrings for a file summary."""
        try:
            tree = ast.parse(content, filename=file_path)
            summary_lines = []
            
            def process_node_body(body_items, indent=""):
                for item in body_items:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        # Get decorators
                        for decorator in getattr(item, 'decorator_list', []):
                            if isinstance(decorator, ast.Name):
                                summary_lines.append(f"{indent}@{decorator.id}")
                            else:
                                summary_lines.append(f"{indent}@decorator")
                        
                        # Add the declaration line
                        if isinstance(item, ast.ClassDef):
                            summary_lines.append(f"{indent}class {item.name}:")
                            # Process class body to find methods
                            process_node_body(item.body, indent + "    ")
                        elif isinstance(item, ast.AsyncFunctionDef):
                            summary_lines.append(f"{indent}async def {item.name}():")
                        else:  # Regular function
                            summary_lines.append(f"{indent}def {item.name}():")
                        
                        # Add docstring if present
                        docstring = ast.get_docstring(item)
                        if docstring:
                            docstring_lines = docstring.strip().split('\n')
                            if len(docstring_lines) == 1:
                                summary_lines.append(f'{indent}    """{docstring_lines[0]}"""')
                            else:
                                summary_lines.append(f'{indent}    """')
                                for line in docstring_lines:
                                    summary_lines.append(f'{indent}    {line}')
                                summary_lines.append(f'{indent}    """')
                        
                        if indent == "":  # Only add empty line after top-level items
                            summary_lines.append("")
            
            # Process the main body of the module
            process_node_body(tree.body)
            return "\n".join(summary_lines)
        except SyntaxError:
            return f"# Could not parse {os.path.basename(file_path)} for summary (SyntaxError)\n"
        except Exception as e:
            return f"# Error parsing {os.path.basename(file_path)} for summary: {e}\n"

    def aggregate(self):
        with open(self.output_file, 'w', encoding='utf-8') as outfile:
            for file_path in self._find_files():
                processed_content = self._process_file(file_path)
                if processed_content:
                    outfile.write(processed_content)
            
            if self.include_metadata:
                outfile.write("\n\n" + "="*20 + " METADATA " + "="*20 + "\n")
                outfile.write(f"Total Files Processed: {self.metadata['total_files']}\n")
                outfile.write(f"Total Lines of Code (LOC): {self.metadata['code_lines']}\n")
                outfile.write(f"Total Comment Lines: {self.metadata['comment_lines']}\n")
                outfile.write(f"Total Blank Lines: {self.metadata['blank_lines']}\n")
                total_code_and_comment = self.metadata['code_lines'] + self.metadata['comment_lines']
                if total_code_and_comment > 0:
                    comment_ratio = (self.metadata['comment_lines'] / total_code_and_comment) * 100
                    outfile.write(f"Comment Ratio: {comment_ratio:.2f}%\n")
                else:
                    outfile.write("Comment Ratio: N/A (no code or comments found)\n")
                outfile.write(f"Total Lines (including blanks): {self.metadata['total_lines']}\n")


        print(f"Aggregated code written to {self.output_file}")
        if self.include_metadata:
             print("Metadata appended to the output file.")

    def compare_files(self, file1: str, file2: str, output_file: Optional[str] = None, context_lines: int = 3) -> str:
        """Compares two code files and shows their differences with clear formatting.
        
        Args:
            file1: Path to the first file
            file2: Path to the second file
            output_file: Optional path to write the diff results to
            context_lines: Number of context lines to include in the diff (default: 3)
            
        Returns:
            String containing the formatted differences
        """
        # Check if files exist
        if not os.path.exists(file1):
            raise FileNotFoundError(f"File not found: {file1}")
        if not os.path.exists(file2):
            raise FileNotFoundError(f"File not found: {file2}")
            
        try:
            # Read file contents
            with open(file1, 'r', encoding='utf-8') as f:
                content1 = f.readlines()
            with open(file2, 'r', encoding='utf-8') as f:
                content2 = f.readlines()
                
            # Generate diff
            diff = difflib.unified_diff(
                content1, 
                content2,
                fromfile=os.path.basename(file1),
                tofile=os.path.basename(file2),
                n=context_lines
            )
            
            # Format the diff based on output format
            diff_text = "".join(diff)
            
            # Add color formatting for better readability
            colored_diff = ""
            for line in diff_text.splitlines(True):
                if line.startswith('+'):
                    colored_diff += f"\033[92m{line}\033[0m"  # Green for additions
                elif line.startswith('-'):
                    colored_diff += f"\033[91m{line}\033[0m"  # Red for deletions
                elif line.startswith('^'):
                    colored_diff += f"\033[36m{line}\033[0m"  # Cyan for change indicators
                elif line.startswith('@@'):
                    colored_diff += f"\033[94m{line}\033[0m"  # Blue for chunk headers
                else:
                    colored_diff += line
                    
            # Write to output file if specified
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(diff_text)
                return f"Diff written to {output_file}"
                
            return colored_diff
            
        except IOError as e:
            raise IOError(f"Error reading or writing files: {e}")
        except Exception as e:
            raise Exception(f"Error comparing files: {e}")

    def compare_runs(self, prev_output: str, current_output: Optional[str] = None, 
                     output_file: Optional[str] = None, context_lines: int = 3) -> str:
        """Compares the current aggregation run with a previous one.
        
        Args:
            prev_output: Path to the previous aggregation output file
            current_output: Path to the current output file (defaults to self.output_file)
            output_file: Optional path to write the diff results to
            context_lines: Number of context lines to include in the diff
            
        Returns:
            String containing the formatted differences
        """
        current = current_output or self.output_file
        
        # Generate the current output file if it doesn't exist yet
        if not os.path.exists(current):
            self.write_to_file(filename=current)
            
        return self.compare_files(prev_output, current, output_file, context_lines)
