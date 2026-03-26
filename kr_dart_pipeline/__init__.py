"""kr-dart-pipeline — ETL from Korean financial data sources into standardized parquets.

Extracts data from DART, KRX, SEIBRO, KFTC, and FSC into 01_Data/processed/*.parquet.
All extractors are idempotent: re-running is safe and skips existing files.

Usage:
    from kr_dart_pipeline import run
    run(market="KOSDAQ", start=2019, end=2023)
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add this package directory to sys.path so that the flat-layout
# pipeline scripts can import each other via bare module names
# (e.g., `import extract_dart as ed` within pipeline.py).
_PKG_DIR = str(Path(__file__).parent)
if _PKG_DIR not in sys.path:
    sys.path.insert(0, _PKG_DIR)

from kr_dart_pipeline._entry import run  # noqa: E402, F401

__version__ = "1.0.0"
__all__ = ["run"]
