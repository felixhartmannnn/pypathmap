# PyPathMap

Visualize Python package dependency trees from any local codebase.

## About

PyPathMap scans a directory and produces a structured tree view of packages and modules.
It is useful for understanding project structure, auditing legacy codebases, or generating package maps for documentation.

## Features

- Text, Markdown, and JSON outputs
- Configurable max depth
- Regex path filtering
- Package stats: total nodes, max depth, average children
- Pure stdlib implementation; no runtime dependencies

## Installation

```bash
git clone https://github.com/example/pypathmap.git
cd pypathmap
python -m pip install -e .
```

## Usage

```bash
pypathmap src/mypackage
pypathmap . --filter __pycache__
pypathmap src/mypackage --format markdown
pypathmap src/mypackage --format json
pypathmap src/mypackage --max-depth 2
```

## Project Structure

```
pypathmap/
  src/pypathmap/
    __init__.py
    core.py
    cli.py
  tests/test_core.py
  pyproject.toml
  README.md
```

## Tags

python, dependency, visualization, tree, tooling, cli, package-structure, ast
