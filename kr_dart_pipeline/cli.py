"""cli.py — Typer CLI for kr-dart-pipeline."""

from __future__ import annotations

from typing import Optional

import typer

app = typer.Typer(
    name="kr-dart-pipeline",
    help="ETL pipeline: extract Korean financial data (DART/KRX/SEIBRO/KFTC/FSC) → parquet.",
    add_completion=False,
)


@app.command()
def run(
    market: str = typer.Option("KOSDAQ", help="Market: KOSDAQ, KOSPI, or KONEX"),
    start: int = typer.Option(2019, help="First fiscal year (inclusive)"),
    end: int = typer.Option(2023, help="Last fiscal year (inclusive)"),
    stage: Optional[str] = typer.Option(
        None,
        help="Single stage: dart | transform | cb_bw (default: dart+transform)",
    ),
    corp_code: Optional[str] = typer.Option(None, help="Run for a single 8-digit DART corp_code"),
    force: bool = typer.Option(False, help="Re-fetch even if output files already exist"),
    rebuild: bool = typer.Option(False, help="Rebuild parquets from cached raw files"),
    sample: Optional[int] = typer.Option(None, help="Limit universe to first N companies"),
    max_minutes: Optional[float] = typer.Option(None, help="Hard wall-clock deadline in minutes"),
    sleep: Optional[float] = typer.Option(None, help="Override inter-request sleep (seconds)"),
    wics_date: Optional[str] = typer.Option(None, help="Pin WICS snapshot date (YYYYMMDD)"),
    scoped: bool = typer.Option(False, help="(cb_bw) Apply M-Score scoping filter"),
    top_n: int = typer.Option(100, help="(cb_bw) Top-N companies in scoped universe"),
    backend: str = typer.Option("pykrx", help="OHLCV backend: pykrx | fdr | yfinance"),
) -> None:
    """Run the ETL pipeline."""
    from kr_dart_pipeline import run as _run
    _run(
        market=market,
        start=start,
        end=end,
        stage=stage,
        corp_code=corp_code,
        force=force,
        rebuild=rebuild,
        sample=sample,
        max_minutes=max_minutes,
        sleep=sleep,
        wics_date=wics_date,
        scoped=scoped,
        top_n=top_n,
        backend=backend,
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
