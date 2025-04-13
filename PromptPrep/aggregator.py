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
from .formatters import get_formatter, BaseFormatter



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
    # Default file size limit: 100 MB
    DEFAULT_MAX_FILE_SIZE_MB = 100.0
    # Default token model (GPT-4's cl100k_base)
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
        line_numbers: bool = False
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
        self.include_metadata = collect_metadata  # Store the flag with a different name to avoid conflict
        self.count_tokens = count_tokens
        self.token_model = token_model
        self.output_format = output_format
        self.line_numbers = line_numbers
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
            self.formatter = get_formatter(self.output_format)
        except (ValueError, ImportError) as e:
            warnings.warn(f"Failed to initialize formatter for format '{self.output_format}': {e}. Falling back to plain text.")
            self.formatter = get_formatter("plain")

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
        """Check if the file size is within the configured limit."""
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / (1024 * 1024)  # Convert to MB
        return file_size_mb <= self.max_file_size_mb

    def count_text_tokens(self, text: str) -> int:
        """Count the number of tokens in a text string using the specified tokenizer."""
        if not self.tokenizer:
            self.tokenizer = tiktoken.get_encoding(self.token_model)
        
        try:
            tokens = self.tokenizer.encode(text)
            return len(tokens)
        except Exception as e:
            warnings.warn(f"Error counting tokens: {e}. Returning estimated count.")
            # Fallback estimation (rough approximation)
            return len(text.split())

    def aggregate_code(self) -> str:
        """Aggregates the directory tree and the content of programming-related files."""
        tree = self.tree_generator.generate(self.directory)
        
        if "Directory not found" in tree:
            error_message = f"Directory not found: {self.directory}"
            return self.formatter.format_error(error_message)

        # --- Count files for progress bar ---
        files_to_process = []
        skipped_files = []
        for root, dirs, files in os.walk(self.directory):
            # Apply directory exclusions early
            rel_path_for_exclusion_check = os.path.relpath(root, self.directory)
            if rel_path_for_exclusion_check == ".":
                rel_path_for_exclusion_check = ""
            
            # Filter excluded directories
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
                    skipped_files.append((rel_file_path, os.path.getsize(file_path) / (1024 * 1024)))
                    continue
                    
                files_to_process.append(file_path)

        # Start with an empty string for aggregated content
        aggregated = ""
        
        # Initialize token counting variables
        total_tokens = 0
        
        # Collect metadata if requested
        metadata_dict = {}
        if self.include_metadata or self.count_tokens:
            metadata_dict = self.collect_metadata()
            if self.count_tokens:
                metadata_dict["token_model"] = self.token_model
                metadata_dict["total_tokens"] = "[placeholder]"
            
            # Format the metadata using the formatter
            if self.include_metadata:
                metadata_section = self.formatter.format_metadata(metadata_dict)
                aggregated += metadata_section + "\n\n"
                
                if self.count_tokens:
                    # Count tokens for metadata section (without the token count line itself)
                    metadata_tokens = self.count_text_tokens(metadata_section)
                    total_tokens += metadata_tokens

        # Format the directory tree
        tree_section = self.formatter.format_directory_tree(tree)
        aggregated += tree_section
        
        if self.count_tokens:
            tree_tokens = self.count_text_tokens(tree_section)
            total_tokens += tree_tokens
            
        # --- Process files with progress bar ---
        for file_path in tqdm(files_to_process, desc="Aggregating files", unit="file", leave=False):
            rel_file_path = os.path.relpath(file_path, self.directory)
            # Format file header
            header = self.formatter.format_file_header(rel_file_path)
            aggregated += header
            
            if self.count_tokens:
                total_tokens += self.count_text_tokens(header)
                
            try:
                with open(file_path, "r", encoding="utf-8", errors='ignore') as f:
                    content = f.read()

                    if not self.include_comments:
                        # More thorough comment removal, including inline comments
                        processed_lines = []
                        for line in content.splitlines():
                            # Split the line at the first #, if any
                            code_part = line.split('#', 1)[0]
                            # If there's something left after stripping, or if it's just whitespace
                            if code_part.strip() or not line.strip():
                                processed_lines.append(code_part.rstrip())
                        content = "\n".join(processed_lines)

                    if self.summary_mode:
                        # Use our improved summary extraction
                        content = self._extract_summary(content, file_path)

                    # Format the code content using the formatter (without line numbers)
                    formatted_content = self.formatter.format_code_content(content, file_path)
                    
                    # Add line numbers only if explicitly requested
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
        
        # Add information about skipped files due to size limit
        if skipped_files:
            skipped_section = self.formatter.format_skipped_files(
                [(path, size_mb) for path, size_mb in skipped_files]
            )
            aggregated += skipped_section
            if self.count_tokens:
                total_tokens += self.count_text_tokens(skipped_section)
        
        # Update the token count in the metadata section if needed
        if self.count_tokens and "[placeholder]" in aggregated:
            # Format the total tokens with thousands separator
            formatted_token_count = f"{total_tokens:,}"
            # Replace the placeholder with the actual count
            aggregated = aggregated.replace("[placeholder]", formatted_token_count)
        
        # For HTML formats, wrap the content in a complete HTML document
        if hasattr(self.formatter, 'get_full_html'):
            title = f"Code Aggregation - {os.path.basename(self.directory)}"
            aggregated = self.formatter.get_full_html(aggregated, title)
        
        return aggregated

    def write_to_file(self, content: Optional[str] = None, filename: Optional[str] = None) -> None:
        """Writes the aggregated content to a file."""
        content = content or self.aggregate_code()
        filename = filename or self.output_file
        
        # If HTML format but filename doesn't have .html extension, add it
        if self.output_format in ["html", "highlighted"] and not filename.lower().endswith(".html"):
            root, _ = os.path.splitext(filename)
            filename = f"{root}.html"
        
        # If Markdown format but filename doesn't have .md extension, add it
        if self.output_format == "markdown" and not filename.lower().endswith((".md", ".markdown")):
            root, _ = os.path.splitext(filename)
            filename = f"{root}.md"
            
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
                
            # Update the output_file attribute to reflect the actual filename used
            self.output_file = filename
        except IOError as e:
            raise IOError(f"Error writing to file {filename}: {e}")

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
        """Collects metadata about the codebase."""
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
                    # Use tokenize for more accurate comment/code distinction
                    g = tokenize.tokenize(io.BytesIO(content.encode('utf-8')).readline)
                    for token_info in g:
                        if token_info.type == tokenize.NL:
                            continue # Handled by line iteration
                        elif token_info.type == tokenize.NEWLINE:
                             processed_lines.append("") # Keep blank lines for structure if not excluding
                             file_blank_lines += 1
                        elif token_info.type == tokenize.COMMENT:
                            if self.include_comments:
                                processed_lines.append(token_info.string)
                            file_comment_lines += 1
                        elif token_info.type == tokenize.ENDMARKER:
                            continue
                        else: # Code tokens (NAME, OP, NUMBER, STRING, etc.)
                             # Reconstruct lines containing code
                             line_num = token_info.start[0] -1 # 0-based index
                             if line_num < len(lines):
                                 current_line = lines[line_num]
                                 # Avoid adding the same line multiple times if it has multiple tokens
                                 if not processed_lines or processed_lines[-1] != current_line:
                                     processed_lines.append(current_line)
                                     file_code_lines += 1 # Count this line as a code line

                except tokenize.TokenError:
                     # Fallback for files that cannot be tokenized (e.g., non-python)
                     # Simple line-based processing as a fallback
                     for line in lines:
                         stripped_line = line.strip()
                         is_comment = stripped_line.startswith('#') # Basic check
                         is_blank = not stripped_line

                         if is_blank:
                             file_blank_lines += 1
                             processed_lines.append(line) # Keep blank lines
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
        """Extracts only function/class declarations and docstrings using AST."""
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
                            summary_lines.append("")  # Add empty line after each top-level function/class
            
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
