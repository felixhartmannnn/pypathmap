"""Unit tests for pypathmap.core."""

import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))

from pypathmap.core import TreeStats, build_tree, collect_stats, is_package_dir, render_text


def test_build_tree_nested_package() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        nested = base / "pkg"
        nested.mkdir(parents=True, exist_ok=True)
        (nested / "__init__.py").write_text("", encoding="utf-8")
        (nested / "module.py").write_text("", encoding="utf-8")

        tree = build_tree(str(nested))

    assert tree is not None
    names = [child.name for child in tree.children]
    assert "module.py" in names


def test_two_children_text() -> None:
    pkg = Path(tempfile.mkdtemp(prefix="pypathmap-"))
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "alpha.py").write_text("", encoding="utf-8")
    (pkg / "beta.py").write_text("", encoding="utf-8")

    text = render_text(build_tree(str(pkg)))
    assert "alpha.py" in text
    assert "beta.py" in text
    assert text.count("├──") + text.count("└──") == 3


def test_package_identifier() -> None:
    assert is_package_dir(Path("/tmp/nonexistent")) is False


def test_stats_counts() -> None:
    pkg = Path(tempfile.mkdtemp(prefix="pypathmap-"))
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "alpha.py").write_text("", encoding="utf-8")
    (pkg / "beta.py").write_text("", encoding="utf-8")

    tree = build_tree(str(pkg))
    assert tree is not None
    stats = TreeStats()
    collect_stats(tree, stats)
    assert stats.nodes == 3
    assert stats.max_depth == 1


def test_build_tree_max_depth() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        (base / "pkg" / "__init__.py").parent.mkdir(parents=True, exist_ok=True)
        (base / "pkg" / "__init__.py").write_text("", encoding="utf-8")
        (base / "pkg" / "a.py").write_text("", encoding="utf-8")
        (base / "pkg" / "nested" / "__init__.py").parent.mkdir(parents=True, exist_ok=True)
        (base / "pkg" / "nested" / "__init__.py").write_text("", encoding="utf-8")
        (base / "pkg" / "nested" / "b.py").write_text("", encoding="utf-8")
        (base / "pkg" / "nested" / "deep" / "__init__.py").parent.mkdir(parents=True, exist_ok=True)
        (base / "pkg" / "nested" / "deep" / "__init__.py").write_text("", encoding="utf-8")
        (base / "pkg" / "nested" / "deep" / "c.py").write_text("", encoding="utf-8")

        shallow = build_tree(str(base / "pkg"), max_depth=1)
        assert shallow is not None
        shallow_text = render_text(shallow)
        assert "a.py" in shallow_text
        assert "nested" in shallow_text
        assert "b.py" not in shallow_text

        deep = build_tree(str(base / "pkg"), max_depth=4)
        assert deep is not None
        deep_text = render_text(deep)
        assert "b.py" in deep_text
        assert "c.py" in deep_text
