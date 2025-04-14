"""
This file helps pytest discover the package properly.
It's especially important in CI environments.
"""
import os
import sys
from pathlib import Path

# Get the absolute path to the project root directory
project_root = Path(__file__).parent.parent.absolute()

# Add the project root to the Python path
sys.path.insert(0, str(project_root))

# Debug information to help diagnose import issues
print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")
print(f"Project root added to path: {project_root}")

# Check if module is importable after adding to path
try:
    import promptprep

    print(f"Successfully imported promptprep from {promptprep.__file__}")
except ImportError as e:
    print(f"Failed to import promptprep: {e}")
    # Try listing the directories to see if the package is there
    print(f"Contents of {project_root}:")
    for item in os.listdir(project_root):
        print(f"  - {item}")

    if os.path.exists(os.path.join(project_root, "promptprep")):
        print("promptprep directory exists, listing contents:")
        for item in os.listdir(os.path.join(project_root, "promptprep")):
            print(f"  - {item}")
