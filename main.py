from __future__ import annotations

import argparse
import os
import shlex
import sys
from dataclasses import dataclass
from datetime import datetime
from logging import Logger
from pathlib import Path
from typing import Dict, List, Optional

from PySide6.QtWidgets import QApplication

from src.cli.cli_interface import CLIInterface, CLIResponse
from src.cli.macro_commands import MacroCommandSet
from src.cli.playback_commands import PlaybackCommandSet
from src.cli.recording_commands import RecordingCommandSet
from src.core.error_handling import CapturedException, ErrorHandler
from src.core.logging_utils import get_logger
from src.core.macro_service import MacroService
from src.export_import.package_service import PackageService
from src.hotkeys.hotkey_service import HotkeyService
from src.models.hotkey import HotkeyActionType
from src.models.user_settings import UserSettings
from src.player.playback_service import PlaybackService
from src.recorder.input_capture import InputCaptureManager
from src.recorder.recording_service import RecordingService
from src.scheduler.scheduling_service import SchedulingService
from src.storage.json_storage import JSONStorageManager
from src.ui.main_window import MainWindow
from src.ui.system_tray import SystemTrayManager
from src.utils.screenshot_service import ScreenshotService
from src.utils.windows_api import WindowsAPIWrapper

DEFAULT_DATA_ENV = "AWESOME_MACRO_DATA_DIR"
DEFAULT_DATA_DIRNAME = ".awesome_python_macro"


@dataclass
class ApplicationContext:
    data_dir: Path
    storage: JSONStorageManager
    macro_service: MacroService
    package_service: PackageService
    playback_service: PlaybackService
    recording_service: RecordingService
    scheduler: SchedulingService
    hotkey_service: HotkeyService
    system_tray: SystemTrayManager
    main_window: MainWindow
    cli: CLIInterface
    error_handler: ErrorHandler
    capture_manager: InputCaptureManager
    screenshot_service: ScreenshotService
    user_settings: UserSettings
    logger: Logger
    captured_errors: List[CapturedException]

    def refresh_state(self) -> None:
        """Refresh UI facades that mirror application state."""
        self.main_window.refresh_macro_list()
        self.system_tray.build_quick_actions()

    def available_commands(self) -> List[str]:
        commands = getattr(self.cli, "_commands", {})
        return sorted(commands.keys())

    def execute_cli_command(self, command_line: str) -> CLIResponse:
        """Execute a CLI command string using the registered command sets."""
        tokens = shlex.split(command_line)
        if not tokens:
            return CLIResponse(ok=False, message="No command provided.")

        command_tokens: List[str] = []
        kwargs: Dict[str, object] = {}
        for token in tokens:
            if "=" in token:
                key, value = token.split("=", 1)
                kwargs[key.replace("-", "_")] = self._coerce_value(value)
            else:
                command_tokens.append(token)

        command_key = " ".join(command_tokens)
        if not command_key:
            return CLIResponse(ok=False, message="Command prefix missing.")

        result: Dict[str, CLIResponse] = {}

        def _invoke() -> None:
            result["response"] = self.cli.execute(command_key, **kwargs)

        self.error_handler.capture(_invoke, context=f"cli:{command_key}")
        response = result.get("response")
        if response is None:
            detail = ""
            if self.captured_errors:
                detail = f" ({self.captured_errors[-1].exception})"
            return CLIResponse(
                ok=False,
                message=f"Command failed due to internal error{detail}.",
            )

        if response.ok:
            self.refresh_state()
        return response

    @staticmethod
    def _coerce_value(value: str) -> object:
        lowered = value.lower()
        if lowered in {"true", "false"}:
            return lowered == "true"
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
        return value


def resolve_data_dir(explicit: Optional[Path] = None) -> Path:
    """Resolve the directory used for persistent application data."""
    if explicit is not None:
        return explicit.expanduser().resolve()

    env_path = os.getenv(DEFAULT_DATA_ENV)
    if env_path:
        return Path(env_path).expanduser().resolve()

    return (Path.home() / DEFAULT_DATA_DIRNAME).resolve()


def build_application(data_dir: Optional[Path] = None) -> ApplicationContext:
    """Create the application context with fully wired services."""
    app = QApplication.instance()
    if app is None:  # pragma: no cover - requires GUI environment
        app = QApplication([])
    resolved_dir = resolve_data_dir(data_dir)
    resolved_dir.mkdir(parents=True, exist_ok=True)

    storage = JSONStorageManager(base_path=resolved_dir)
    macro_service = MacroService(storage_manager=storage)
    package_service = PackageService(storage_manager=storage)
    playback_service = PlaybackService()
    capture_manager = InputCaptureManager()
    screenshot_service = ScreenshotService()
    recording_service = RecordingService(
        capture_manager=capture_manager,
        macro_service=macro_service,
        screenshot_service=screenshot_service,
    )
    scheduler = SchedulingService(
        macro_service=macro_service,
        playback_service=playback_service,
    )
    windows_api = WindowsAPIWrapper()
    hotkey_service = HotkeyService(windows_api=windows_api)
    user_settings = storage.load_settings()
    main_window = MainWindow(
        macro_service=macro_service,
        playback_service=playback_service,
        hotkey_service=hotkey_service,
        settings=user_settings,
        storage_manager=storage,
    )
    system_tray = SystemTrayManager(
        macro_service=macro_service,
        playback_service=playback_service,
    )
    main_window.attach_system_tray(system_tray)
    cli = CLIInterface()
    cli.register_commands(RecordingCommandSet(recording_service))
    cli.register_commands(PlaybackCommandSet(playback_service, macro_service))
    cli.register_commands(MacroCommandSet(macro_service))

    logger = get_logger("application")
    captured_errors: List[CapturedException] = []
    error_handler = ErrorHandler()

    def _log_error(captured: CapturedException) -> None:
        captured_errors.append(captured)
        context = f" ({captured.context})" if captured.context else ""
        logger.error(
            "Unhandled exception%s: %s",
            context,
            captured.exception,
            exc_info=captured.exception,
        )

    error_handler.add_listener(_log_error)

    context = ApplicationContext(
        data_dir=resolved_dir,
        storage=storage,
        macro_service=macro_service,
        package_service=package_service,
        playback_service=playback_service,
        recording_service=recording_service,
        scheduler=scheduler,
        hotkey_service=hotkey_service,
        system_tray=system_tray,
        main_window=main_window,
        cli=cli,
        error_handler=error_handler,
        capture_manager=capture_manager,
        screenshot_service=screenshot_service,
        user_settings=user_settings,
        logger=logger,
        captured_errors=captured_errors,
    )

    _register_hotkey_handlers(context)
    context.refresh_state()
    logger.info("Application initialized with data directory %s", resolved_dir)
    return context


def _register_hotkey_handlers(context: ApplicationContext) -> None:
    """Wire hotkey actions to core services for quick automation flows."""

    def _play_macro(hotkey) -> None:
        macro_id = hotkey.macro_id
        if not macro_id:
            context.logger.warning(
                "Play macro hotkey triggered without an associated macro id.",
            )
            return
        macro = context.macro_service.get_macro(macro_id)
        if not macro:
            context.logger.warning(
                "Macro %s not found for hotkey %s",
                macro_id,
                hotkey.key_combination,
            )
            return
        context.logger.info(
            "Playing macro %s via hotkey %s",
            macro.name,
            hotkey.key_combination,
        )
        context.main_window.play_macro(macro.id)

    def _start_recording(_hotkey) -> None:
        name = f"Quick Recording {datetime.now().strftime('%Y%m%d-%H%M%S')}"
        try:
            session = context.recording_service.start_recording(name=name)
        except Exception as exc:  # pragma: no cover - defensive guard
            context.logger.warning("Unable to start recording via hotkey: %s", exc)
            return
        context.logger.info("Recording session %s started via hotkey", session.session_id)

    def _stop_recording(_hotkey) -> None:
        try:
            macro = context.recording_service.stop_recording()
        except Exception as exc:  # pragma: no cover - defensive guard
            context.logger.warning("Unable to stop recording via hotkey: %s", exc)
            return
        if macro:
            context.logger.info("Recording %s saved via hotkey", macro.name)
            context.refresh_state()
        else:
            context.logger.info("No active recording session to stop.")

    def _show_window(_hotkey) -> None:
        context.logger.info("Hotkey triggered main window refresh")
        context.main_window.show()
        context.main_window.raise_()
        context.main_window.activateWindow()
        context.refresh_state()

    def _hide_window(_hotkey) -> None:
        context.logger.info("Hotkey triggered main window hide request")
        context.main_window.hide()

    def _minimize_to_tray(_hotkey) -> None:
        context.logger.info("Hotkey triggered minimize-to-tray request")
        context.main_window.hide()
        context.system_tray.show_notification(
            "Awesome Macro",
            "Application minimized to the system tray.",
        )

    hotkey_service = context.hotkey_service
    hotkey_service.register_action_handler(HotkeyActionType.PLAY_MACRO, _play_macro)
    hotkey_service.register_action_handler(HotkeyActionType.START_RECORDING, _start_recording)
    hotkey_service.register_action_handler(HotkeyActionType.STOP_RECORDING, _stop_recording)
    hotkey_service.register_action_handler(HotkeyActionType.SHOW_WINDOW, _show_window)
    hotkey_service.register_action_handler(HotkeyActionType.HIDE_WINDOW, _hide_window)
    hotkey_service.register_action_handler(HotkeyActionType.MINIMIZE_TO_TRAY, _minimize_to_tray)


def run_cli_loop(context: ApplicationContext) -> None:
    """Launch an interactive CLI shell for manual experimentation."""
    print("Awesome Macro CLI ready. Type 'help' to list commands, 'exit' to quit.")
    while True:
        try:
            raw = input("awesome-macro> ")
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            break

        command_line = raw.strip()
        if not command_line:
            continue
        if command_line.lower() in {"exit", "quit"}:
            break
        if command_line.lower() in {"help", "?"}:
            print("Available commands:")
            for name in context.available_commands():
                print(f"  {name}")
            print("Arguments use key=value syntax, e.g. 'macro create name=Demo'.")
            continue

        response = context.execute_cli_command(command_line)
        status = "OK" if response.ok else "ERR"
        print(f"[{status}] {response.message}")


def list_macros(context: ApplicationContext) -> None:
    """Print a simple summary of stored macros to stdout."""
    context.refresh_state()
    macros = context.macro_service.list_macros()
    if not macros:
        print("No macros found.")
        return
    for macro in macros:
        print(
            f"{macro.id} - {macro.name} "
            f"({len(macro.actions)} actions, {macro.total_duration_ms:.0f}ms)",
        )


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Awesome Macro application entry point")
    parser.add_argument("--data-dir", type=Path, help="Override the default data directory")
    parser.add_argument(
        "--cli",
        dest="cli_command",
        help="Execute a single CLI command (quote the command) and exit",
    )
    parser.add_argument(
        "--list-macros",
        action="store_true",
        help="List stored macros and exit",
    )
    parser.add_argument(
        "--run-scheduler",
        action="store_true",
        help="Run pending schedules once and exit",
    )

    args = parser.parse_args(argv)
    context = build_application(data_dir=args.data_dir)

    if args.run_scheduler:
        context.scheduler.run_pending()
        return 0

    if args.cli_command:
        response = context.execute_cli_command(args.cli_command)
        print(response.message)
        return 0 if response.ok else 1

    if args.list_macros:
        list_macros(context)
        return 0

    if sys.stdin.isatty():
        run_cli_loop(context)
    else:
        context.logger.info(
            "No interactive terminal detected; initialization complete. Use --cli for commands.",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
