"""
Configure pytest for the promptprep test suite.
This file helps pytest find the promptprep package correctly during test runs.
"""
import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to ensure the promptprep package can be imported
# This is particularly helpful in CI environments
sys.path.insert(0, str(Path(__file__).parent.parent))