from __future__ import annotations

from pathlib import Path

from src.core.quickstart import QuickstartValidator


def test_quickstart_validator_detects_sections():
    base = Path(__file__).resolve().parents[2]
    quickstart = base / "specs" / "001-comprehensive-macro-recording" / "quickstart.md"
    validator = QuickstartValidator.from_markdown(quickstart.read_text(encoding="utf-8"))
    report = validator.validate()

    assert report.success
    assert "Application Startup" in report.sections
    assert report.total_checks >= 3
