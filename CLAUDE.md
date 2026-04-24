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


---

**Working notes** (regulatory analysis, legal compliance research, or anything else not appropriate for this public repo) belong in the gitignored working directory of the coordination hub. Engineering docs (API patterns, test strategies, run logs) stay here.

---

## NEVER commit to this repo

This repository is **public**. Before staging or writing any new file, check the list below. If the content matches any item, route it to the gitignored working directory of the coordination hub instead, NOT to this repo.

**Hard NO list:**

1. **Any API key, token, or credential — even a truncated fingerprint.** This includes Anthropic key fingerprints (sk-ant-...), AWS keys (AKIA...), GitHub tokens (ghp_...), DART/SEIBRO/KFTC API keys, FRED keys. Even partial / display-truncated keys (e.g. "sk-ant-api03-...XXXX") leak the org-to-key linkage and must not be committed.
2. **Payment / billing data of any kind.** Card numbers (full or last-four), invoice IDs, receipt numbers, order numbers, billing-portal URLs, Stripe/Anthropic/PayPal account states, monthly-spend caps, credit balances.
3. **Vendor support correspondence.** Subject lines, body text, ticket IDs, or summaries of correspondence with Anthropic / GitHub / Vercel / DART / any vendor's support team.
4. **Named third-party outreach targets.** Specific company names, hedge-fund names, audit-firm names, regulator-individual names appearing in a planning, pitch, or outreach context. Engineering content discussing Korean financial institutions in a neutral domain context (e.g. "DART is the FSS disclosure system") is fine; planning text naming them as a sales target is not.
5. **Commercial-positioning memos.** Documents discussing buyer segments, monetization models, pricing strategy, competitor analysis, market positioning, or go-to-market plans. Research methodology and technical roadmaps are fine; commercial strategy is not.
6. **Files matching the leak-prevention .gitignore patterns** (*_prep.md, *_billing*, *_outreach*, *_strategy*, *_positioning*, *_pricing*, *_buyer*, *_pitch*, product_direction.md, etc.). If you find yourself wanting to write a file with one of these names, that is a signal that the content belongs in the hub working directory.

**When in doubt:** put the content in the hub working directory (gitignored), not this repo. It is always safe to add later. It is expensive to remove after force-pushing — orphaned commits remain resolvable on GitHub for weeks.

GitHub Push Protection is enabled on this repo and will reject pushes containing well-known credential patterns. That is a backstop, not the primary defense — write-time discipline is.
