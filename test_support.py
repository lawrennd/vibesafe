"""
Test helpers for the VibeSafe repository.

This repo "dogfoods" its installer: canonical tooling lives under `templates/`,
and installation copies those templates into runtime locations (e.g. `scripts/`,
`backlog/`, `tenets/`) in a user project.

For unit tests, we want to test the canonical template code directly without
requiring that the installer has been run.
"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path
from types import ModuleType


def load_module_from_path(module_name: str, file_path: Path) -> ModuleType:
    """
    Load a Python module from a file path under a specific module name.

    This supports legacy import/patch targets like "scripts.whats_next" while
    executing the canonical source file from `templates/`.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(str(file_path))

    # Ensure parent packages exist (e.g. "scripts" for "scripts.whats_next").
    parts = module_name.split(".")
    for i in range(1, len(parts)):
        pkg_name = ".".join(parts[:i])
        if pkg_name not in sys.modules:
            pkg = types.ModuleType(pkg_name)
            pkg.__path__ = []  # mark as package for import machinery
            sys.modules[pkg_name] = pkg

    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec for {module_name} from {file_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

