"""PyPathMap core builder."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class Node:
    name: str
    path: str
    children: List["Node"] = field(default_factory=list)
    is_package: bool = True


@dataclass
class TreeStats:
    nodes: int = 0
    max_depth: int = 0
    children_counts: List[int] = field(default_factory=list)

    def record_node(self, depth: int) -> None:
        self.nodes += 1
        self.max_depth = max(self.max_depth, depth)

    def record_children(self, count: int) -> None:
        self.children_counts.append(count)

    @property
    def avg_children(self) -> float:
        if not self.children_counts:
            return 0.0
        return sum(self.children_counts) / len(self.children_counts)


def is_package_dir(path: Path) -> bool:
    if not path.is_dir():
        return False
    has_init = (path / "__init__.py").is_file()
    has_py = any(
        child.is_file() and child.suffix == ".py" for child in path.iterdir()
    )
    return has_init or has_py


def build_tree(
    root_path: str,
    max_depth: int = 10,
    filter_pattern: Optional[str] = None,
    current_depth: int = 0,
    origin: Optional[Path] = None,
) -> Optional[Node]:
    """Build an import package tree from a filesystem path."""
    if origin is None:
        origin = Path(root_path).resolve()
    abs_path = Path(root_path).resolve()
    if not abs_path.is_dir() or not is_package_dir(abs_path):
        return None

    rel = str(abs_path.relative_to(origin)) or "."
    node = Node(name=rel, path=str(abs_path), is_package=True)

    try:
        entries = sorted(abs_path.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))
    except PermissionError:
        return node

    for entry in entries:
        if entry.name.startswith(".") or entry.name.startswith("__"):
            continue
        if entry.name in {"setup.py", "setup.cfg", "pyproject.toml", "README.md", "LICENSE"}:
            continue
        if entry.name in {"__pycache__", ".venv", "node_modules", ".git", "dist", "build"}:
            continue
        if filter_pattern and re.search(filter_pattern, str(entry)):
            continue

        if entry.is_dir() and is_package_dir(entry):
            if current_depth + 1 > max_depth:
                continue
            child = build_tree(
                str(entry),
                max_depth=max_depth,
                filter_pattern=filter_pattern,
                current_depth=current_depth + 1,
                origin=origin,
            )
            if child is not None:
                node.children.append(child)
        elif (
            entry.is_file()
            and entry.suffix == ".py"
            and entry.stem != "__init__"
        ):
            if current_depth + 1 > max_depth:
                continue
            child = Node(
                name=entry.name,
                path=str(entry),
                children=[],
                is_package=False,
            )
            node.children.append(child)

    return node


def render_text(node: Node) -> str:
    lines: List[str] = []

    def walk(n: Node, prefix: str, last: bool) -> None:
        connector = "└── " if last else "├── "
        suffix = "/" if n.is_package else ""
        lines.append(f"{prefix}{connector}{n.name}{suffix}")
        child_prefix = prefix + ("    " if last else "│   ")
        if n.children:
            for i, child in enumerate(n.children):
                walk(child, child_prefix, i == len(n.children) - 1)

    walk(node, "", True)
    return "\n".join(lines)


def collect_stats(node: Node, stats: TreeStats, depth: int = 0) -> None:
    stats.record_node(depth)
    stats.record_children(len(node.children))
    for child in node.children:
        collect_stats(child, stats, depth + 1)


def render_markdown(node: Node, stats: Optional[TreeStats] = None) -> str:
    lines: List[str] = []
    lines.append("```")
    lines.extend(_md_lines(node, "", 0))
    lines.append("```")
    if stats is not None:
        lines.append("")
        lines.append(f"- **Total nodes**: {stats.nodes}")
        lines.append(f"- **Max depth**: {stats.max_depth}")
    return "\n".join(lines)


def _md_lines(node: Node, prefix: str, depth: int) -> List[str]:
    result: List[str] = []
    connector = "- " if prefix == "" else "  - "
    suffix = "/" if node.is_package else ""
    result.append(f"{prefix}{connector}**{node.name}**{suffix}")
    if node.children:
        extension = "  "
        for i, child in enumerate(node.children):
            result.extend(_md_lines(child, prefix=f"{prefix}{extension}", depth=depth + 1))
    return result


def render_json(node: Node, stats: Optional[TreeStats] = None) -> str:
    import json

    def to_dict(n: Node) -> dict:
        return {
            "name": n.name,
            "path": n.path,
            "is_package": n.is_package,
            "children": [to_dict(c) for c in n.children],
        }

    payload = {
        "tree": to_dict(node),
        "stats": {
            "total_nodes": stats.nodes if stats is not None else 0,
            "max_depth": stats.max_depth if stats is not None else 0,
            "avg_children": round(stats.avg_children, 1) if stats is not None else 0.0,
        },
    }
    return json.dumps(payload, indent=2)
