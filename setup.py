#!/usr/bin/env python3
"""
Setup script for promptprep package.
This file ensures that the package can be installed correctly on all platforms.
"""
import os
import sys
from setuptools import setup

# Debug information
print(f"Current directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir('.')}")
print(f"promptprep exists: {os.path.exists('promptprep')}")
print(
    f"promptprep is dir: {os.path.isdir('promptprep') if os.path.exists('promptprep') else 'N/A'}"
)

# Make sure we're in the correct directory
if os.path.exists("promptprep") and os.path.isdir("promptprep"):
    packages = ["promptprep"]
    print("Using explicit package: promptprep")
else:
    # If the directory doesn't exist, this will cause a clear error
    print("ERROR: promptprep directory not found!")
    sys.exit(1)

setup(
    name="promptprep",
    packages=packages,
    # Other metadata is read from pyproject.toml
)
