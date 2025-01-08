# depscan 🔍

A Python dependency analyzer inspired by Black's implementation that automatically discovers and extracts third-party imports from your Python projects. It scans your codebase to identify external dependencies while filtering out project-internal imports.

## Features ✨

- Follows Black's approach to traverse Python files
- Smart package name resolution (e.g., `PIL` → `pillow`, `cv2` → `opencv-python`)
- Filters out both standard library and project-internal imports
- Handles common import name mismatches
- Generates `requirements.txt` file
- Parallel processing for faster scanning

⚠️ Note: The tool may occasionally fail to identify some dependencies due to complex import patterns or dynamic imports.

## Installation 📦

```bash
pip install -U depscan
```

## Usage 🚀

You can use depscan either as a module or directly as a command (like Black):

```bash
# As a command (recommended)
depscan src/
depscan .                    # Current directory
depscan src/ tests/         # Multiple paths

# As a module
python -m depscan src/
python -m depscan .
```

Options:
```bash
depscan src/ --no-save     # Don't generate requirements file
depscan src/ --workers 4   # Specify number of parallel workers
```

## How it Works 🛠️

1. Traverses Python files using Black's file discovery approach
2. Uses AST parsing to safely extract imports
3. Filters out standard library and project-internal imports
4. Maps common import aliases to their correct PyPI package names
5. Generates a clean requirements file

## Output 📝

The tool will:
1. Show all scanned files
2. List discovered third-party dependencies
3. Generate a `requirements.txt` file (or `requirements-depscan.txt` if the former exists)

## Known Limitations 🚧

- May not detect dependencies from dynamic imports
- Some complex import patterns might be missed
- Package name mapping might not cover all cases

## Contributing 🤝

Found a bug or want to improve the package name mapping? Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

[MIT](LICENSE)