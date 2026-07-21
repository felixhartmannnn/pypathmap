# Documentation

## Formats

### Text
Default tree view with box-drawing characters.

### Markdown
Bullet list inside a code block, with optional stats.

### JSON
Machine-readable tree with stats payload.

## Behavior Notes

- A directory is treated as a package if it contains `__init__.py` or any `.py` file.
- `__init__.py` files are not listed as standalone module nodes.
- Entries starting with `.` or `__` are skipped by default.
- Common build/cache directories are always excluded.
