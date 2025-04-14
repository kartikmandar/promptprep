"""
This file helps pytest discover the package properly.
It's especially important in CI environments.
"""
import os
import sys
from pathlib import Path

# Add the parent directory to sys.path
# This ensures the package can be imported during testing
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))