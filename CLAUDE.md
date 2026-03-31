# kr-dart-pipeline
> ETL pipeline: 15 extractors pulling from DART, KRX, SEIBRO, KFTC, and FSC → parquet outputs consumed by krff-shell, kr-anomaly-scoring, and kr-stat-tests.

## Install & Test
```bash
uv sync
uv run pytest tests/ -v
```

## Architecture

Package root: `kr_dart_pipeline/`

- `extract_*.py` — 15 extractor scripts (one per data source/table). Each writes a `.parquet` to the processed data directory.
- `pipeline.py` — Orchestration: runs all extractors in dependency order via `run_all()`.
- `transform.py` — Shared transformation helpers (amount parsing, unit normalization).
- `_pipeline_helpers.py` — `fetch_with_backoff()`, `parse_amount()`, `_parse_krw()`, `_detect_unit_multiplier()`.
- `cli.py` — `uv run krff-pipeline run` entry point.
- `build_isin_map.py` — Builds `bond_isin_map.parquet` from FSC bond data.
- `_entry.py` — Public entry point re-exported by `__init__.py` as `kr_dart_pipeline.run()`. Delegates to `kr_dart_pipeline.pipeline.run()` via lazy importlib (avoids heavy imports at package load time).

Data output path: resolved by `kr_forensic_core.paths.data_dir()` — defaults to `01_Data/processed/` relative to the repo root.

## Conventions
- Package manager: `uv`
- Build system: hatchling
- Test command: `uv run pytest tests/ -v`
- All paths resolved via `kr_forensic_core.paths.data_dir()` — never hardcoded
- No `sys.path` manipulation — all imports are absolute package imports

## Key Decisions
- `sys.path.insert` was removed from `__init__.py` in March 2026. It had been shadowing the krff-shell root `cli.py` by injecting the installed package directory first. Fix: all bare module imports converted to `kr_dart_pipeline.*` absolute imports.
- Each extractor is standalone — can be run individually (`uv run python -m kr_dart_pipeline.extract_price_volume`) or via `pipeline.py`.
- SEIBRO extractor (`extract_seibro.py`, `extract_seibro_repricing.py`) stubs remain — SEIBRO API (공공데이터포털 dataset 15001145) returning `resultCode=99` as of 2026-03-26. ETA: end of April 2026.

## Known Gaps

| Gap | Why | Status |
|-----|-----|--------|
| SEIBRO extractors not functional | 공공데이터포털 revising StockSvc API; `resultCode=99` — see XB-002 | Blocked — ETA end of April 2026 |
| No integration test for full `pipeline.run_all()` | Requires live DART API keys in CI | Deferred |
| `_entry.py` bare importlib call | Fixed 2026-03-31: `"pipeline"` → `"kr_dart_pipeline.pipeline"` | Resolved |
