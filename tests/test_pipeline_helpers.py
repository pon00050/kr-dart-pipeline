"""Functional tests for kr_dart_pipeline._pipeline_helpers."""

from unittest.mock import MagicMock, patch

import pytest

from kr_dart_pipeline._pipeline_helpers import (
    _detect_unit_multiplier,
    _parse_krw,
    fetch_with_backoff,
    parse_amount,
)


# ── parse_amount ──────────────────────────────────────────────────────────────

def test_parse_amount_none():
    assert parse_amount(None) is None


def test_parse_amount_empty_string():
    assert parse_amount("") is None


def test_parse_amount_dash():
    assert parse_amount("-") is None


def test_parse_amount_comma_integer():
    assert parse_amount("1,234,567") == 1234567.0


def test_parse_amount_parenthetical_negative():
    assert parse_amount("(500,000)") == -500000.0


def test_parse_amount_nan_string():
    assert parse_amount("nan") is None


def test_parse_amount_whitespace():
    assert parse_amount("  1234  ") == 1234.0


def test_parse_amount_negative():
    assert parse_amount("-1234") == -1234.0


# ── _parse_krw ────────────────────────────────────────────────────────────────

def test_parse_krw_none():
    assert _parse_krw(None) is None


def test_parse_krw_empty_string():
    assert _parse_krw("") is None


def test_parse_krw_comma_integer():
    assert _parse_krw("1,234") == 1234


def test_parse_krw_parenthetical_negative():
    assert _parse_krw("(500)") == -500


def test_parse_krw_unit_multiplier():
    assert _parse_krw("1,000", unit_multiplier=1000) == 1_000_000


def test_parse_krw_non_numeric():
    assert _parse_krw("abc") is None


# ── _detect_unit_multiplier ───────────────────────────────────────────────────

def test_detect_unit_multiplier_cheonwon():
    assert _detect_unit_multiplier("재무제표 천원 단위") == 1000


def test_detect_unit_multiplier_parenthetical():
    assert _detect_unit_multiplier("(단위: 천원)") == 1000


def test_detect_unit_multiplier_absent():
    assert _detect_unit_multiplier("<html><body>재무정보</body></html>") == 1


def test_detect_unit_multiplier_only_after_2000_chars():
    prefix = "x" * 2001
    html = prefix + "천원"
    assert _detect_unit_multiplier(html) == 1


def test_detect_unit_multiplier_at_boundary():
    # "천원" is 2 chars; placing it at positions 1998-1999 keeps it inside the slice
    prefix = "x" * 1998
    html = prefix + "천원"
    assert _detect_unit_multiplier(html) == 1000


# ── fetch_with_backoff ────────────────────────────────────────────────────────

def _make_response(data: dict) -> MagicMock:
    resp = MagicMock()
    resp.json.return_value = data
    return resp


def test_fetch_with_backoff_success_first_call():
    ok_resp = _make_response({"status": "000", "items": [1, 2, 3]})
    with patch("requests.get", return_value=ok_resp) as mock_get:
        result = fetch_with_backoff("https://example.com", {}, max_retries=2, base_delay=0.0)
    assert result == {"status": "000", "items": [1, 2, 3]}
    assert mock_get.call_count == 1


def test_fetch_with_backoff_retries_on_020_then_succeeds():
    rate_limit_resp = _make_response({"status": "020", "message": "rate limit"})
    ok_resp = _make_response({"status": "000", "items": []})
    with patch("requests.get", side_effect=[rate_limit_resp, ok_resp]) as mock_get:
        with patch("time.sleep"):
            result = fetch_with_backoff("https://example.com", {}, max_retries=2, base_delay=0.1)
    assert result == {"status": "000", "items": []}
    assert mock_get.call_count == 2


def test_fetch_with_backoff_non_020_raises_immediately():
    with patch("requests.get", side_effect=ConnectionError("network down")):
        with pytest.raises(ConnectionError):
            fetch_with_backoff("https://example.com", {}, max_retries=3, base_delay=0.0)


def test_fetch_with_backoff_exhausted_retries_raises():
    rate_limit_resp = _make_response({"status": "020"})
    with patch("requests.get", return_value=rate_limit_resp):
        with patch("time.sleep"):
            with pytest.raises(Exception, match="020"):
                fetch_with_backoff("https://example.com", {}, max_retries=2, base_delay=0.0)
