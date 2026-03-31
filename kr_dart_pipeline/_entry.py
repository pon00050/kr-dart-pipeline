"""_entry.py — Public entry point re-exported by __init__.py as kr_dart_pipeline.run().

Delegates to kr_dart_pipeline.pipeline.run() via importlib to avoid importing
the full pipeline module (and its heavy extractor imports) at package load time.
"""

from __future__ import annotations

import importlib


def run(*args, **kwargs):
    """Run the ETL pipeline. Delegates to kr_dart_pipeline.pipeline.run()."""
    pipeline = importlib.import_module("kr_dart_pipeline.pipeline")
    return pipeline.run(*args, **kwargs)
