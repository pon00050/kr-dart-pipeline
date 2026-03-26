"""kr-dart-pipeline — ETL from Korean financial data sources into standardized parquets.

Extracts data from DART, KRX, SEIBRO, KFTC, and FSC into 01_Data/processed/*.parquet.
All extractors are idempotent: re-running is safe and skips existing files.

Usage:
    from kr_dart_pipeline import run
    run(market="KOSDAQ", start=2019, end=2023)
"""

from __future__ import annotations

from kr_dart_pipeline._entry import run  # noqa: F401

__version__ = "1.0.0"
__all__ = ["run"]
