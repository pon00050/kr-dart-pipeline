"""_entry.py — Thin wrapper that imports pipeline.run() from the flat-layout scripts.

The pipeline scripts use bare module imports (import extract_dart as ed) that
work because kr_dart_pipeline/__init__.py adds the package directory to sys.path.
"""

from __future__ import annotations

import importlib


def run(*args, **kwargs):
    """Run the ETL pipeline. Delegates to pipeline.run() inside the package."""
    pipeline = importlib.import_module("pipeline")
    return pipeline.run(*args, **kwargs)
