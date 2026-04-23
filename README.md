# kr-dart-pipeline

**[Read the full write-up →](https://ronanwrites.vercel.app/manuals/forensic-platform-architecture)**

ETL pipeline for Korean financial data — DART, KRX, SEIBRO, KFTC, and FSC → standardized parquets.

Part of the [forensic accounting toolkit](https://github.com/pon00050/forensic-accounting-toolkit) ecosystem.

## Usage

```bash
# Full Phase 1 run (DART financials + transform)
kr-dart-pipeline run --market KOSDAQ --start 2019 --end 2023

# Single stage
kr-dart-pipeline run --stage dart
kr-dart-pipeline run --stage transform
kr-dart-pipeline run --stage cb_bw

# Sample mode (first 50 companies, fast)
kr-dart-pipeline run --market KOSDAQ --start 2022 --end 2023 --sample 50
```

```python
from kr_dart_pipeline import run
run(market="KOSDAQ", start=2019, end=2023)
```

## Install

```bash
uv add git+https://github.com/pon00050/kr-dart-pipeline
```

## Outputs

All outputs land in `01_Data/processed/` (set `KRFF_DATA_DIR` to override):

| File | Description |
|------|-------------|
| `company_financials.parquet` | Annual IFRS financials (DART) |
| `cb_bw_events.parquet` | Convertible bond / bond-with-warrant events |
| `price_volume.parquet` | OHLCV price and volume (KRX) |
| `corp_ticker_map.parquet` | DART corp_code ↔ KRX ticker mapping |
| `officer_holdings.parquet` | Officer shareholding changes |
| `disclosures.parquet` | Material disclosure filings |
| `major_holders.parquet` | Large shareholder reports (5%+) |
| `bondholder_register.parquet` | SEIBRO bondholder register |
| `revenue_schedule.parquet` | Depreciation/revenue schedules |
| `bond_isin_map.parquet` | Bond ISIN ↔ corp_code mapping |
