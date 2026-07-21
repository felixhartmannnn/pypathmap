"""PyPathMap CLI."""
from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from pypathmap.core import (
    Node,
    TreeStats,
    build_tree,
    collect_stats,
    render_json,
    render_markdown,
    render_text,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pypathmap",
        description="Visualize Python package dependency trees from the filesystem.",
    )
    parser.add_argument("path", help="Root package path to scan")
    parser.add_argument(
        "--format",
        choices=["text", "markdown", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=10,
        help="Maximum tree depth to recurse (default: 10)",
    )
    parser.add_argument(
        "--filter",
        dest="filter_pattern",
        help="Regex pattern to exclude paths",
    )
    return parser


def format_output(node: Node, fmt: str) -> str:
    stats = TreeStats()
    collect_stats(node, stats)
    if fmt == "text":
        return render_text(node)
    if fmt == "markdown":
        return render_markdown(node, stats)
    if fmt == "json":
        return render_json(node, stats)
    raise ValueError(f"Unsupported format: {fmt}")


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    root_path = args.path
    fmt = args.format
    max_depth = args.max_depth
    filter_pattern = args.filter_pattern

    root = __import__("pathlib").Path(root_path)
    if not root.is_dir():
        print(f"Error: '{root_path}' is not a directory.", file=sys.stderr)
        return 1

    tree = build_tree(
        root_path,
        max_depth=max_depth,
        filter_pattern=filter_pattern,
    )

    if tree is None:
        print(f"Error: '{root_path}' does not appear to be a Python package.", file=sys.stderr)
        return 1

    print(format_output(tree, fmt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
