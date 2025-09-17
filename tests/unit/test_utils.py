from __future__ import annotations

import pytest

from src.models.action import Action
from src.models.macro import Macro
from src.utils import file_utils
from src.utils.validation import ValidationError, validate_macro


def test_ensure_directory(tmp_path):
    target = tmp_path / "nested" / "path"
    file_utils.ensure_directory(target)
    assert target.exists()
    assert target.is_dir()


def test_atomic_write_and_read_json(tmp_path):
    payload = {"value": 42}
    target = tmp_path / "data.json"
    file_utils.atomic_write_json(target, payload)
    loaded = file_utils.read_json(target)
    assert loaded == payload


def test_validate_macro_rejects_empty_name():
    macro = Macro.create(name="Valid")
    macro.name = ""
    with pytest.raises(ValidationError):
        validate_macro(macro)


def test_validate_macro_accepts_valid_macro():
    macro = Macro.create(name="Valid")
    macro.add_action(Action.delay(macro_id=macro.id, duration_ms=10))
    validate_macro(macro)
