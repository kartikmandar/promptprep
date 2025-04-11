import argparse
import os
import sys
from PromptPrep.aggregator import CodeAggregator

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Aggregate code files into a master file with a directory tree."
    )
    parser.add_argument(
        "-c",
        "--clipboard",
        action="store_true",
        help="Copy aggregated content to the clipboard instead of writing to a file."
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        default=os.getcwd(),
        help="The directory to start aggregation from. Defaults to the current directory."
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        default="full_code.txt",
        help="Name of the output file. Defaults to full_code.txt."
    )
    parser.add_argument(
        "-i",
        "--include-files",
        type=str,
        default="",
        help="Comma-separated list of files to include. If not provided, all files are included."
    )
    parser.add_argument(
        "-x",
        "--extensions",
        type=str,
        default="",
        help="Comma-separated list of programming extensions to use. Replaces the default set if provided."
    )
    parser.add_argument(
        "-e",
        "--exclude-dirs",
        type=str,
        default="",
        help="Comma-separated list of directories to exclude. Replaces the default set if provided."
    )
    parser.add_argument(
        "-m",
        "--max-file-size",
        type=float,
        default=100.0,
        help="Maximum file size in MB to include. Files larger than this will be skipped. Defaults to 100 MB."
    )
    parser.add_argument(
        "--summary-mode",
        action="store_true",
        help="Include only function/class declarations and docstrings."
    )
    parser.add_argument(
        "--include-comments",
        action="store_true",
        default=True,
        help="Include comments in the aggregated output. Defaults to True."
    )
    parser.add_argument(
        "--no-include-comments",
        dest="include_comments",
        action="store_false",
        help="Exclude comments from the aggregated output."
    )
    parser.add_argument(
        "--metadata",
        action="store_true",
        help="Collect and append codebase metadata (LOC, comment ratio, etc.)."
    )
    parser.add_argument(
        "--count-tokens",
        action="store_true",
        help="Count tokens in the output file and include in metadata."
    )
    parser.add_argument(
        "--token-model",
        type=str,
        default="cl100k_base",
        help="The tokenizer model to use for counting tokens. Common options: cl100k_base (for GPT-4), p50k_base (for GPT-3)."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    include_files = {f.strip() for f in args.include_files.split(",") if f.strip()}
    programming_extensions = {e.strip() for e in args.extensions.split(",") if e.strip()}
    exclude_dirs = {d.strip() for d in args.exclude_dirs.split(",") if d.strip()}

    try:
        aggregator = CodeAggregator(
            directory=args.directory,
            output_file=args.output_file,
            include_files=include_files,
            programming_extensions=programming_extensions if programming_extensions else None,
            exclude_dirs=exclude_dirs if exclude_dirs else None,
            max_file_size_mb=args.max_file_size,
            summary_mode=args.summary_mode,
            include_comments=args.include_comments,
            collect_metadata=args.metadata,
            count_tokens=args.count_tokens,
            token_model=args.token_model
        )

        if args.clipboard:
            if aggregator.copy_to_clipboard():  # pragma: no cover
                print("Aggregated content copied to the clipboard successfully.")  # pragma: no cover
            else:
                print("Failed to copy content to the clipboard.")  # pragma: no cover
                raise SystemExit(1)  # pragma: no cover
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
    main() # pragma: no cover

