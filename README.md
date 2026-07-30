# PyPathMap

Visualize Python package dependency trees from any local codebase.

## About

PyPathMap scans a directory and produces a structured tree view of packages and modules. It is useful for understanding project structure, auditing legacy codebases, or generating package maps for documentation.

## Features

- Text, Markdown, and JSON outputs
- Configurable max depth
- Regex path filtering
- Package stats: total nodes, max depth, average children
- Pure stdlib implementation; no runtime dependencies
- Works via CLI or as an installed package

## Installation

```bash
git clone https://github.com/felixhartmannnn/pypathmap.git
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

When installed as a package, the CLI is available through the `pypathmap` entry point. The package also supports invoking as a module with `python -m pypathmap`.

## Project Structure

```
pypathmap/
  src/pypathmap/
    __init__.py
    __main__.py
    cli.py
    core.py
  tests/
    test_core.py
  pyproject.toml
  README.md
```

## Topics

python, dependency, visualization, tree, tooling, cli, package-structure

## Repository

https://github.com/felixhartmannnn/pypathmap
