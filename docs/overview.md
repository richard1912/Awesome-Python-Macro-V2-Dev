# Macro Recording Application Overview

This repository contains a reference implementation of a desktop-oriented macro recording and playback toolkit. The code base is organized into distinct modules for data models, storage, input capture, playback, services, user interface facades, scheduling, hotkey integration, and command-line tooling.

## Key Components

- **Data Models (`src/models/`)**: Dataclasses describe macros, actions, screenshots, hotkeys, schedules, macro packages, and user settings. Each model provides serialization helpers to simplify persistence and export workflows.
- **Storage Layer (`src/storage/`)**: The `JSONStorageManager` persists macros and user settings to JSON files and exposes simple iteration helpers to support lazy loading of large macro collections.
- **Core Services (`src/core/`)**: `MacroService` coordinates CRUD operations and validation. Additional helpers cover quickstart validation, logging, and centralized error handling.
- **Input & Playback (`src/recorder/`, `src/player/`)**: Lightweight abstractions transform captured keyboard and mouse events into rich action records and replay them with deterministic timing.
- **Automation Utilities (`src/hotkeys/`, `src/scheduler/`, `src/export_import/`)**: Modules manage global hotkeys, scheduled execution, and import/export of macro bundles.
- **User Interface Stubs (`src/ui/`)**: Headless facades mimic PySide6 widgets enabling deterministic tests that verify state management without a GUI environment.
- **CLI (`src/cli/`)**: Command sets expose automation-friendly interfaces for recording, playback, and macro management.

## Development Notes

- All functionality is driven by automated tests located under `tests/` with separate suites for contracts, integration, unit, and performance validation.
- The project targets Python 3.11+ and provides formatting and linting configuration for `black`, `flake8`, and `isort` via `pyproject.toml`.
- A lightweight build script (`scripts/build.py`) demonstrates how to package the application with PyInstaller.
