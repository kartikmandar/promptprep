#!/usr/bin/env python3
"""
Setup script for promptprep package.
This file ensures that the package can be installed correctly on all platforms.
"""
import os
from setuptools import setup, find_packages

# Make sure we're in the correct directory
if os.path.exists("promptprep") and os.path.isdir("promptprep"):
    packages = ["promptprep"]
elif os.path.exists("PromptPrep") and os.path.isdir("PromptPrep"):
    # Handle case mismatch between local and remote
    packages = ["PromptPrep"]
else:
    # Fallback to automatic discovery
    packages = find_packages()

setup(
    name="promptprep",
    packages=packages,
    # Other metadata is read from pyproject.toml
)
