from __future__ import annotations

from main import ApplicationContext, build_application, resolve_data_dir


def test_build_application_initializes_services(tmp_path, qapp):
    context = build_application(tmp_path)
    assert isinstance(context, ApplicationContext)
    assert context.data_dir == tmp_path.resolve()
    assert "macro create" in context.available_commands()


def test_execute_cli_command_creates_macro(tmp_path, qapp):
    context = build_application(tmp_path)
    response = context.execute_cli_command("macro create name=EntryPointTest")
    assert response.ok
    names = [macro.name for macro in context.macro_service.list_macros()]
    assert "EntryPointTest" in names


def test_execute_cli_command_handles_errors(tmp_path, qapp):
    context = build_application(tmp_path)

    def _boom(**_: object):
        raise RuntimeError("boom")

    context.cli._commands["macro boom"] = _boom
    response = context.execute_cli_command("macro boom")
    assert not response.ok
    assert "internal error" in response.message.lower()
    assert context.captured_errors


def test_resolve_data_dir_prefers_env(monkeypatch, tmp_path):
    expected = tmp_path / "custom"
    monkeypatch.setenv("AWESOME_MACRO_DATA_DIR", str(expected))
    resolved = resolve_data_dir()
    assert resolved == expected.resolve()
