from __future__ import annotations

from src.core.error_handling import ErrorHandler
from src.core.logging_utils import get_logger


def test_logging_utils_returns_named_logger():
    logger = get_logger("tests")
    logger.debug("message")
    assert logger.name.endswith("tests")


def test_error_handler_captures_exceptions():
    handler = ErrorHandler()
    captured = []
    handler.add_listener(captured.append)

    def _failing() -> None:
        raise ValueError("boom")

    handler.capture(_failing)
    assert captured and isinstance(captured[0].exception, ValueError)
