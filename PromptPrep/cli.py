import argparse
import os
import sys
from promptprep.aggregator import CodeAggregator
from promptprep.config import ConfigManager

if sys.platform != "win32":
    # Import TUI function only if not on Windows
    from promptprep.tui import select_files_interactive
else:
    # Define a dummy function for Windows
    # It should match the signature and return type of the real one
    def select_files_interactive(directory: str) -> tuple[set[str], set[str], bool]:
        print("Error: Interactive mode is not supported on Windows.", file=sys.stderr)
        # Return values indicating cancellation/no selection
        return set(), set(), False


def parse_arguments() -> argparse.Namespace:
    """Sets up and handles command-line interface options for the code aggregation tool."""
    parser = argparse.ArgumentParser(
        description="Aggregate code files into a master file with a directory tree."
    )

    # Group for exclusive commands: standard aggregation or diff
    action_group = parser.add_mutually_exclusive_group()

    # Add the main --diff trigger to the *mutually exclusive* group
    action_group.add_argument(
        "--diff",
        metavar="PREV_FILE",
        dest="prev_file",
        type=str,
        help="Compare a previous aggregation file with the current one. Cannot be used with other action flags.",  # Example help text
    )

    # Create a separate argument group for *visual* organization of diff options in help
    diff_options_group = parser.add_argument_group(
        "File Diff Options (used with --diff)"
    )

    # Add the diff-specific options to the *visual* group
    diff_options_group.add_argument(
        "--diff-context",
        type=int,
        default=3,
        help="Number of context lines to include in diff (default: 3)",
    )
    diff_options_group.add_argument(
        "--diff-output", type=str, help="Write diff to specified file instead of stdout"
    )

    # Standard arguments
    parser.add_argument(
        "-c",
        "--clipboard",
        action="store_true",
        help="Copy aggregated content to the clipboard instead of writing to a file.",
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        default=os.getcwd(),
        help="The directory to start aggregation from. Defaults to the current directory.",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        default="full_code.txt",
        help="Name of the output file. Defaults to full_code.txt.",
    )
    parser.add_argument(
        "-i",
        "--include-files",
        type=str,
        default="",
        help="Comma-separated list of files to include. If not provided, all files are included.",
    )
    parser.add_argument(
        "-x",
        "--extensions",
        type=str,
        default="",
        help="Comma-separated list of programming extensions to use. Replaces the default set if provided.",
    )
    parser.add_argument(
        "-e",
        "--exclude-dirs",
        type=str,
        default="",
        help="Comma-separated list of directories to exclude. Replaces the default set if provided.",
    )
    parser.add_argument(
        "-m",
        "--max-file-size",
        type=float,
        default=100.0,
        help="Maximum file size in MB to include. Files larger than this will be skipped. Defaults to 100 MB.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Use interactive TUI mode to select files/directories to include or exclude.",
    )
    parser.add_argument(
        "--incremental",
        action="store_true",
        help="Only process files that have changed since the last run.",
    )
    parser.add_argument(
        "--last-run-timestamp",
        type=float,
        default=None,
        help="Timestamp of the last run (Unix epoch time). Required when using --incremental.",
    )
    parser.add_argument(
        "--summary-mode",
        action="store_true",
        help="Include only function/class declarations and docstrings.",
    )
    parser.add_argument(
        "--include-comments",
        action="store_true",
        default=True,
        help="Include comments in the aggregated output. Defaults to True.",
    )
    parser.add_argument(
        "--no-include-comments",
        dest="include_comments",
        action="store_false",
        help="Exclude comments from the aggregated output.",
    )
    parser.add_argument(
        "--metadata",
        action="store_true",
        help="Collect and append codebase metadata (LOC, comment ratio, etc.).",
    )
    parser.add_argument(
        "--count-tokens",
        action="store_true",
        help="Count tokens in the output file and include in metadata.",
    )
    parser.add_argument(
        "--token-model",
        type=str,
        default="cl100k_base",
        help="The tokenizer model to use for counting tokens. Common options: cl100k_base (for GPT-4), p50k_base (for GPT-3).",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["plain", "markdown", "html", "highlighted", "custom"],
        default="plain",
        help="Output format. Options: plain (default), markdown, html, highlighted and custom.",
    )
    parser.add_argument(
        "--line-numbers",
        action="store_true",
        help="Include line numbers in the output. Defaults to False.",
    )
    parser.add_argument(
        "--template-file",
        type=str,
        default=None,
        help="Path to a custom template file (required for --format custom).",
    )
    parser.add_argument(
        "--save-config",
        type=str,
        metavar="CONFIG_FILE",
        nargs="?",
        const="default",
        help="Save current configuration to a file. Uses default location (~/.promptprep/config.json) if no path is provided.",
    )
    parser.add_argument(
        "--load-config",
        type=str,
        metavar="CONFIG_FILE",
        nargs="?",
        const="default",
        help="Load configuration from a file. Uses default location (~/.promptprep/config.json) if no path is provided.",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for the code aggregation tool."""
    args = parse_arguments()

    # Load saved configuration if requested
    if args.load_config:
        try:
            config_file = None if args.load_config == "default" else args.load_config
            config_dict = ConfigManager.load_config(config_file)
            args = ConfigManager.apply_config_to_args(config_dict, args)
            if config_file:
                print(f"Configuration loaded from '{config_file}'.")
            else:
                print("Configuration loaded from default location.")
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    include_files = set()
    exclude_dirs = set()
    should_continue = True

    # Ensure template is provided for custom format
    if args.format == "custom" and not args.template_file:
        print(
            "Error: --template-file is required when using --format custom",
            file=sys.stderr,
        )
        sys.exit(1)

    # Let users select files interactively if requested
    if args.interactive:
        print("Starting interactive file selection...")
        include_files, exclude_dirs, should_continue = select_files_interactive(
            args.directory
        )

        if should_continue:
            print(
                f"Selected {len(include_files)} files to include and {len(exclude_dirs)} directories to exclude."
            )
        else:
            print("Interactive selection canceled. No files will be processed.")
            return
    else:
        include_files = {f.strip() for f in args.include_files.split(",") if f.strip()}
        exclude_dirs = {d.strip() for d in args.exclude_dirs.split(",") if d.strip()}

    programming_extensions = {
        e.strip() for e in args.extensions.split(",") if e.strip()
    }

    # Save current configuration if requested
    if args.save_config:
        try:
            config_file = None if args.save_config == "default" else args.save_config
            saved_path = ConfigManager.save_config(args, config_file)
            print(f"Configuration saved to '{saved_path}'.")

            # Exit if only saving config
            if len(sys.argv) == 2 and "--save-config" in sys.argv[1]:
                return
            if len(sys.argv) == 3 and "--save-config" in sys.argv[1:]:
                return
        except IOError as e:
            print(f"Error saving configuration: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        aggregator = CodeAggregator(
            directory=args.directory,
            output_file=args.output_file,
            include_files=include_files,
            programming_extensions=(
                programming_extensions if programming_extensions else None
            ),
            exclude_dirs=exclude_dirs if exclude_dirs else None,
            max_file_size_mb=args.max_file_size,
            summary_mode=args.summary_mode,
            include_comments=args.include_comments,
            collect_metadata=args.metadata,
            count_tokens=args.count_tokens,
            token_model=args.token_model,
            output_format=args.format,
            line_numbers=args.line_numbers,
            template_file=args.template_file,
            incremental=args.incremental,
            last_run_timestamp=args.last_run_timestamp,
        )

        # Handle file comparison if requested
        if hasattr(args, "prev_file") and args.prev_file:
            if not os.path.exists(args.prev_file):
                print(
                    f"Error: Previous file not found: {args.prev_file}", file=sys.stderr
                )
                sys.exit(1)

            try:
                # Generate current output if needed
                if not os.path.exists(args.output_file):
                    print(
                        f"Current output file '{args.output_file}' does not exist. Generating it..."
                    )
                    aggregator.write_to_file()

                # Show differences between files
                diff_result = aggregator.compare_files(
                    file1=args.prev_file,
                    file2=args.output_file,
                    output_file=args.diff_output,
                    context_lines=args.diff_context,
                )

                if args.diff_output:
                    print(diff_result)
                else:
                    print(
                        f"Diff between {os.path.basename(args.prev_file)} and {os.path.basename(args.output_file)}:"
                    )
                    print(diff_result)
                return
            except Exception as e:
                print(f"Error generating diff: {e}", file=sys.stderr)
                sys.exit(1)
        # Handle regular aggregation
        elif args.clipboard:
            if aggregator.copy_to_clipboard():
                print("Aggregated content copied to the clipboard successfully.")
            else:
                print("Failed to copy content to the clipboard.")
                raise SystemExit(1)
        else:
            aggregator.write_to_file()
            print(f"Aggregated file '{args.output_file}' created successfully.")
    except FileNotFoundError as e:
        print(f"Error: Directory not found: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error: File error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()  # pragma: no cover
