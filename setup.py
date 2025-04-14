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
print(f"PromptPrep exists: {os.path.exists('PromptPrep')}")

# Make sure we're in the correct directory
if os.path.exists("promptprep") and os.path.isdir("promptprep"):
    packages = ["promptprep"]
    print("Using explicit package: promptprep")
elif os.path.exists("PromptPrep") and os.path.isdir("PromptPrep"):
    # Handle case mismatch between local and remote
    packages = ["PromptPrep"]
    print("Using explicit package: PromptPrep")
    # Create a symlink for compatibility
    if not os.path.exists("promptprep"):
        print("Creating symlink from PromptPrep to promptprep")
        try:
            # On Unix systems
            os.symlink("PromptPrep", "promptprep")
        except OSError:
            # On Windows or if symlink fails
            print("Symlink creation failed, copying directory instead")
            import shutil

            shutil.copytree("PromptPrep", "promptprep")
else:
    # If the directory doesn't exist, this will cause a clear error
    print("ERROR: Neither promptprep nor PromptPrep directory found!")
    print(f"Current directory contents: {os.listdir('.')}")
    sys.exit(1)

setup(
    name="promptprep",
    packages=packages,
    # Other metadata is read from pyproject.toml
)
