#!/bin/bash

# Reminder to update version
echo "Current version in pyproject.toml:"
grep "version = " pyproject.toml
echo ""
read -p "Have you updated the version number in pyproject.toml? (y/n) " answer

if [ "$answer" != "y" ]; then
    echo "Please update the version number in pyproject.toml first!"
    exit 1
fi

# Install required tools
pip install build twine

# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
python -m build

# Upload to PyPI
python -m twine upload dist/* 