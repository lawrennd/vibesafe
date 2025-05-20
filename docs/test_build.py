"""Test script to verify Sphinx documentation builds correctly."""

import os
import subprocess
import sys
from pathlib import Path

def test_build():
    """Test that the documentation builds without errors."""
    docs_dir = Path(__file__).parent
    source_dir = docs_dir / 'source'
    build_dir = docs_dir / '_build'
    
    # Ensure we're in the docs directory
    os.chdir(docs_dir)
    
    try:
        # Run sphinx-build with -W flag to treat warnings as errors
        result = subprocess.run(
            ['sphinx-build', '-W', '-b', 'html', str(source_dir), str(build_dir)],
            capture_output=True,
            text=True,
            check=True
        )
        print("Documentation built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print("Error building documentation:", file=sys.stderr)
        print(e.stdout, file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        return False

if __name__ == '__main__':
    sys.exit(0 if test_build() else 1) 