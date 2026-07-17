"""Command-line interface for image dataset inspection."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from image_dataset_inspector.inspector import inspect_directory
from image_dataset_inspector.reporting import write_csv_report


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""
    parser = argparse.ArgumentParser(
        prog="image-dataset-inspector",
        description="Inspect JPEG and PNG datasets and write a CSV report.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser(
        "inspect",
        help="Inspect images below a directory.",
    )
    inspect_parser.add_argument("input", type=Path, help="Directory containing images.")
    inspect_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Destination CSV path.",
    )
    inspect_parser.set_defaults(handler=_run_inspect)
    return parser


def _run_inspect(args: argparse.Namespace) -> int:
    try:
        results = inspect_directory(args.input)
    except (NotADirectoryError, OSError):
        print("Error: the input path must be a readable directory.", file=sys.stderr)
        return 2

    try:
        write_csv_report(results, args.output)
    except OSError:
        print("Error: the CSV report could not be written.", file=sys.stderr)
        return 1

    valid_count = sum(result.status == "valid" for result in results)
    unreadable_count = len(results) - valid_count
    print(f"Scanned: {len(results)}")
    print(f"Valid: {valid_count}")
    print(f"Unreadable: {unreadable_count}")
    print(f"Report: {args.output}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
