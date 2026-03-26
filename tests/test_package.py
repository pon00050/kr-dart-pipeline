"""Smoke tests: package importable, CLI entry point exists, all scripts present."""

import importlib
import sys
from pathlib import Path


def test_package_importable():
    import kr_dart_pipeline
    assert kr_dart_pipeline.__version__ == "1.0.0"


def test_run_function_importable():
    from kr_dart_pipeline import run
    assert callable(run)


def test_cli_module_importable():
    from kr_dart_pipeline.cli import app
    assert app is not None


def test_all_pipeline_scripts_present():
    """Ensure all 19 original pipeline scripts are present in the package."""
    pkg_dir = Path(__file__).resolve().parents[1] / "kr_dart_pipeline"
    expected = {
        "_pipeline_helpers.py",
        "build_isin_map.py",
        "extract_bondholder_register.py",
        "extract_cb_bw.py",
        "extract_corp_actions.py",
        "extract_corp_ticker_map.py",
        "extract_dart.py",
        "extract_depreciation_schedule.py",
        "extract_disclosures.py",
        "extract_kftc.py",
        "extract_krx.py",
        "extract_major_holders.py",
        "extract_officer_holdings.py",
        "extract_price_volume.py",
        "extract_revenue_schedule.py",
        "extract_seibro.py",
        "extract_seibro_repricing.py",
        "pipeline.py",
        "transform.py",
    }
    present = {f.name for f in pkg_dir.glob("*.py") if not f.name.startswith("_") or f.name == "_pipeline_helpers.py"}
    missing = expected - present
    assert not missing, f"Missing pipeline scripts: {missing}"


def test_pipeline_module_importable():
    """pipeline.py must be importable (the orchestrator)."""
    pipeline = importlib.import_module("kr_dart_pipeline.pipeline")
    assert hasattr(pipeline, "run")


def test_no_krff_imports():
    """None of the pipeline scripts should import from krff (delivery shell)."""
    pkg_dir = Path(__file__).resolve().parents[1] / "kr_dart_pipeline"
    violations = []
    for py_file in pkg_dir.glob("*.py"):
        text = py_file.read_text(encoding="utf-8", errors="replace")
        if "from krff" in text or "import krff" in text:
            violations.append(py_file.name)
    assert not violations, f"Scripts import from krff (delivery shell): {violations}"
