from __future__ import annotations

import logging
from typing import Optional


_LOGGING_CONFIGURED = False


def _configure_logging() -> None:
    global _LOGGING_CONFIGURED
    if not _LOGGING_CONFIGURED:
        logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(name)s: %(message)s")
        _LOGGING_CONFIGURED = True


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    _configure_logging()
    logger = logging.getLogger(f"awesome_macro.{name}")
    if level is not None:
        logger.setLevel(level)
    return logger


__all__ = ["get_logger"]
