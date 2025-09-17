# Tasks: Comprehensive Macro Recording Application

**Input**: Design documents from `/specs/001-comprehensive-macro-recording/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 3.1: Setup
- [x] T001 Create project structure per implementation plan
- [x] T002 Initialize Python project with PySide6, pynput, pywin32 dependencies
- [x] T003 [P] Configure black, flake8, isort linting and formatting tools

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**

### Contract Tests
- [x] T004 [P] Contract test recording API in tests/contract/test_recording_api.py
- [x] T005 [P] Contract test playback API in tests/contract/test_playback_api.py
- [x] T006 [P] Contract test macro management API in tests/contract/test_macro_management_api.py
- [x] T007 [P] Contract test hotkey API in tests/contract/test_hotkey_api.py

### Integration Tests
- [x] T008 [P] Integration test recording workflow in tests/integration/test_recording_workflow.py
- [x] T009 [P] Integration test playback workflow in tests/integration/test_playback_workflow.py
- [x] T010 [P] Integration test hotkey management in tests/integration/test_hotkey_management.py
- [x] T011 [P] Integration test macro organization in tests/integration/test_macro_organization.py
- [x] T012 [P] Integration test export/import in tests/integration/test_export_import.py
- [x] T013 [P] Integration test scheduling system in tests/integration/test_scheduling.py
- [x] T014 [P] Integration test system tray integration in tests/integration/test_system_tray.py
- [x] T015 [P] Integration test visual overlay system in tests/integration/test_overlay_system.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)

### Data Models
- [x] T016 [P] Macro model in src/models/macro.py
- [x] T017 [P] Action model in src/models/action.py
- [x] T018 [P] Screenshot model in src/models/screenshot.py
- [x] T019 [P] Hotkey model in src/models/hotkey.py
- [x] T020 [P] Schedule model in src/models/schedule.py
- [x] T021 [P] Macro Package model in src/models/macro_package.py
- [x] T022 [P] User Settings model in src/models/user_settings.py

### Storage Layer
- [x] T023 [P] JSON storage manager in src/storage/json_storage.py
- [x] T024 [P] File system utilities in src/utils/file_utils.py
- [x] T025 [P] Data validation utilities in src/utils/validation.py

### Core Services
- [x] T026 [P] Recording service in src/recorder/recording_service.py
- [x] T027 [P] Playback service in src/player/playback_service.py
- [x] T028 [P] Hotkey service in src/hotkeys/hotkey_service.py
- [x] T029 [P] Macro management service in src/core/macro_service.py
- [x] T030 [P] Scheduling service in src/scheduler/scheduling_service.py
- [x] T031 [P] Export/import service in src/export_import/package_service.py

### Input Capture System
- [x] T032 [P] Input capture manager in src/recorder/input_capture.py
- [x] T033 [P] Keyboard input handler in src/recorder/keyboard_handler.py
- [x] T034 [P] Mouse input handler in src/recorder/mouse_handler.py
- [x] T035 [P] Screenshot capture service in src/utils/screenshot_service.py

### Windows Integration
- [x] T036 [P] Windows API wrapper in src/utils/windows_api.py
- [x] T037 [P] DPI awareness handler in src/utils/dpi_handler.py
- [x] T038 [P] System tray manager in src/ui/system_tray.py

### GUI Components
- [x] T039 [P] Main window in src/ui/main_window.py
- [x] T040 [P] Macro list widget in src/ui/macro_list_widget.py
- [x] T041 [P] Macro editor dialog in src/ui/macro_editor_dialog.py
- [x] T042 [P] Action overlay system in src/ui/action_overlay.py
- [x] T043 [P] Settings dialog in src/ui/settings_dialog.py
- [x] T044 [P] Hotkey configuration dialog in src/ui/hotkey_dialog.py

### CLI Interface
- [x] T045 [P] CLI command interface in src/cli/cli_interface.py
- [x] T046 [P] Recording CLI commands in src/cli/recording_commands.py
- [x] T047 [P] Playback CLI commands in src/cli/playback_commands.py
- [x] T048 [P] Macro management CLI commands in src/cli/macro_commands.py

## Phase 3.4: Integration
- [x] T049 Connect recording service to input capture system
- [x] T050 Connect playback service to action execution system
- [x] T051 Connect hotkey service to Windows API
- [x] T052 Connect GUI components to core services
- [x] T053 Connect CLI interface to all services
- [x] T054 Connect scheduling service to background execution
- [x] T055 Connect export/import service to file system
- [x] T056 Connect system tray to main application
- [ ] T057 Connect logging system to all components
- [ ] T058 Connect error handling to all components

## Phase 3.5: Polish
- [x] T059 [P] Unit tests for models in tests/unit/test_models.py
- [x] T060 [P] Unit tests for services in tests/unit/test_services.py
- [x] T061 [P] Unit tests for utilities in tests/unit/test_utils.py
- [x] T062 [P] Unit tests for GUI components in tests/unit/test_ui.py
- [x] T063 Performance tests for timing accuracy (<10ms latency)
- [x] T064 Performance tests for memory usage with large macro sets
- [x] T065 [P] Update documentation in docs/
- [ ] T066 Remove code duplication and optimize
- [x] T067 Run quickstart validation scenarios
- [x] T068 Create build script for PyInstaller executable

## Dependencies
- Tests (T004-T015) before implementation (T016-T048)
- Models (T016-T022) before services (T023-T031)
- Services before integration (T049-T058)
- Integration before polish (T059-T068)
- Input capture (T032-T035) before recording service (T026)
- Windows integration (T036-T038) before system tray (T044)
- GUI components (T039-T044) before main application integration (T052)

## Parallel Execution Examples

### Launch T004-T007 together (Contract Tests):
```
Task: "Contract test recording API in tests/contract/test_recording_api.py"
Task: "Contract test playback API in tests/contract/test_playback_api.py"
Task: "Contract test macro management API in tests/contract/test_macro_management_api.py"
Task: "Contract test hotkey API in tests/contract/test_hotkey_api.py"
```

### Launch T008-T015 together (Integration Tests):
```
Task: "Integration test recording workflow in tests/integration/test_recording_workflow.py"
Task: "Integration test playback workflow in tests/integration/test_playback_workflow.py"
Task: "Integration test hotkey management in tests/integration/test_hotkey_management.py"
Task: "Integration test macro organization in tests/integration/test_macro_organization.py"
Task: "Integration test export/import in tests/integration/test_export_import.py"
Task: "Integration test scheduling system in tests/integration/test_scheduling.py"
Task: "Integration test system tray integration in tests/integration/test_system_tray.py"
Task: "Integration test visual overlay system in tests/integration/test_overlay_system.py"
```

### Launch T016-T022 together (Data Models):
```
Task: "Macro model in src/models/macro.py"
Task: "Action model in src/models/action.py"
Task: "Screenshot model in src/models/screenshot.py"
Task: "Hotkey model in src/models/hotkey.py"
Task: "Schedule model in src/models/schedule.py"
Task: "Macro Package model in src/models/macro_package.py"
Task: "User Settings model in src/models/user_settings.py"
```

### Launch T023-T031 together (Core Services):
```
Task: "JSON storage manager in src/storage/json_storage.py"
Task: "File system utilities in src/utils/file_utils.py"
Task: "Data validation utilities in src/utils/validation.py"
Task: "Recording service in src/recorder/recording_service.py"
Task: "Playback service in src/player/playback_service.py"
Task: "Hotkey service in src/hotkeys/hotkey_service.py"
Task: "Macro management service in src/core/macro_service.py"
Task: "Scheduling service in src/scheduler/scheduling_service.py"
Task: "Export/import service in src/export_import/package_service.py"
```

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task
   
2. **From Data Model**:
   - Each entity → model creation task [P]
   - Relationships → service layer tasks
   
3. **From User Stories**:
   - Each story → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Tests → Models → Services → Endpoints → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [x] All contracts have corresponding tests (4 contract files → 4 test tasks)
- [x] All entities have model tasks (7 entities → 7 model tasks)
- [x] All tests come before implementation (T004-T015 before T016+)
- [x] Parallel tasks truly independent (different files, no shared dependencies)
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts
- Follow TDD principles: Red → Green → Refactor
- All GUI components use PySide6 (Qt6)
- All Windows integration uses pywin32
- All input capture uses pynput, keyboard, mouse libraries
- All data storage uses JSON with pathlib
