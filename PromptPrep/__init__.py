from .aggregator import CodeAggregator, DirectoryTreeGenerator
from .tui import select_files_interactive, FileSelector
from .formatters import (
    BaseFormatter,
    PlainTextFormatter,
    MarkdownFormatter,
    HtmlFormatter,
    HighlightedFormatter,
    get_formatter
)
from .config import ConfigManager

import importlib.metadata

try:
    __version__ = importlib.metadata.version("promptprep")
except importlib.metadata.PackageNotFoundError:
    # Handle case where package is not installed (e.g., running from source)
    __version__ = "0.0.0-dev"

__all__ = [
    "CodeAggregator",
    "DirectoryTreeGenerator",
    "select_files_interactive",
    "FileSelector",
    "BaseFormatter",
    "PlainTextFormatter",
    "MarkdownFormatter",
    "HtmlFormatter",
    "HighlightedFormatter",
    "get_formatter",
    "ConfigManager"
]
