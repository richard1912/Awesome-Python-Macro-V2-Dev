# Data Model: Comprehensive Macro Recording Application

**Date**: 2024-12-19  
**Branch**: `001-comprehensive-macro-recording`  
**Context**: Core entities and relationships for macro recording system

## Core Entities

### Macro
**Purpose**: Represents a complete automation sequence containing multiple actions  
**Attributes**:
- `id`: Unique identifier (UUID)
- `name`: User-defined name for the macro
- `description`: Optional description of macro purpose
- `created_at`: Timestamp of creation
- `modified_at`: Timestamp of last modification
- `version`: Version number for tracking changes
- `tags`: Array of tags for categorization
- `is_favorite`: Boolean flag for quick access
- `playback_speed`: Multiplier for playback speed (default 1.0)
- `loop_count`: Number of times to repeat (0 = infinite)
- `loop_interval`: Delay between loop iterations (seconds)

**Relationships**:
- Has many `Action` entities
- Has one `Screenshot` per action
- Belongs to `User` (implicit single-user application)

**Validation Rules**:
- Name must be non-empty and unique
- Version must be positive integer
- Playback speed must be > 0 and <= 10.0
- Loop count must be >= 0
- Loop interval must be >= 0

**State Transitions**:
- Draft → Active (when first action added)
- Active → Archived (when marked for deletion)
- Active → Modified (when actions edited)

### Action
**Purpose**: Individual recorded event (keyboard or mouse) with timing and parameters  
**Attributes**:
- `id`: Unique identifier (UUID)
- `macro_id`: Foreign key to Macro
- `action_type`: Enum (keyboard_press, keyboard_release, mouse_click, mouse_move, mouse_scroll, delay)
- `timestamp`: Relative time from macro start (milliseconds)
- `key_code`: Keyboard key code (for keyboard actions)
- `key_name`: Human-readable key name
- `modifier_keys`: Array of modifier keys (Ctrl, Alt, Shift, Win)
- `mouse_button`: Mouse button (left, right, middle, wheel)
- `x_coordinate`: Mouse X position (for mouse actions)
- `y_coordinate`: Mouse Y position (for mouse actions)
- `scroll_direction`: Scroll direction and amount (for scroll actions)
- `delay_duration`: Delay duration in milliseconds (for delay actions)
- `comment`: Optional user comment for documentation

**Relationships**:
- Belongs to `Macro`
- Has one `Screenshot` (captured at action time)

**Validation Rules**:
- Timestamp must be >= 0 and <= macro duration
- Coordinates must be within screen bounds
- Key codes must be valid keyboard keys
- Mouse buttons must be valid options
- Delay duration must be >= 0 and <= 60000 (60 seconds max)

### Screenshot
**Purpose**: Visual context captured at the time of action recording  
**Attributes**:
- `id`: Unique identifier (UUID)
- `action_id`: Foreign key to Action
- `macro_id`: Foreign key to Macro (for quick access)
- `image_data`: Base64-encoded image data
- `image_format`: Image format (PNG, JPEG)
- `width`: Image width in pixels
- `height`: Image height in pixels
- `dpi`: DPI setting when captured
- `captured_at`: Timestamp of capture
- `file_path`: Optional file path for large images

**Relationships**:
- Belongs to `Action`
- Belongs to `Macro` (for organization)

**Validation Rules**:
- Image data must be valid base64 encoding
- Dimensions must be > 0
- DPI must be > 0 and <= 300
- File path must exist if specified

### Hotkey
**Purpose**: Configurable key combination that triggers specific macro operations  
**Attributes**:
- `id`: Unique identifier (UUID)
- `key_combination`: String representation of key combination (e.g., "Ctrl+Shift+F9")
- `action_type`: Enum (start_recording, stop_recording, play_macro, show_window, hide_window, minimize_to_tray)
- `macro_id`: Foreign key to Macro (for play_macro action)
- `is_enabled`: Boolean flag for enabling/disabling
- `is_global`: Boolean flag for system-wide registration
- `conflict_resolution`: Enum (prompt_user, auto_resolve, ignore)

**Relationships**:
- May belong to `Macro` (for macro-specific hotkeys)
- Belongs to `User` (implicit single-user application)

**Validation Rules**:
- Key combination must be valid and unique
- Macro ID required for play_macro action type
- Conflict resolution must be valid option

### Schedule
**Purpose**: Time-based trigger configuration for automatic macro execution  
**Attributes**:
- `id`: Unique identifier (UUID)
- `macro_id`: Foreign key to Macro
- `name`: User-defined name for the schedule
- `is_enabled`: Boolean flag for enabling/disabling
- `start_time`: Initial execution time
- `end_time`: Optional end time for schedule
- `recurrence_type`: Enum (once, daily, weekly, monthly, custom)
- `recurrence_pattern`: JSON object with recurrence details
- `timezone`: Timezone for schedule execution
- `max_executions`: Maximum number of executions (0 = unlimited)
- `execution_count`: Current execution count
- `last_executed`: Timestamp of last execution
- `next_execution`: Timestamp of next scheduled execution

**Relationships**:
- Belongs to `Macro`
- Belongs to `User` (implicit single-user application)

**Validation Rules**:
- Start time must be in the future
- End time must be after start time if specified
- Recurrence pattern must be valid for recurrence type
- Max executions must be >= 0

### Macro Package
**Purpose**: Exportable container holding one or more macros with metadata for sharing  
**Attributes**:
- `id`: Unique identifier (UUID)
- `name`: Package name
- `version`: Package version
- `description`: Package description
- `author`: Package author information
- `created_at`: Package creation timestamp
- `exported_at`: Export timestamp
- `macro_ids`: Array of macro IDs included in package
- `metadata`: JSON object with additional package information
- `file_path`: Path to exported package file
- `file_size`: Size of package file in bytes

**Relationships**:
- Contains many `Macro` entities
- Belongs to `User` (implicit single-user application)

**Validation Rules**:
- Name must be non-empty
- Version must follow semantic versioning
- Macro IDs must be valid and exist
- File path must be valid if specified

### User Settings
**Purpose**: Persistent configuration data including preferences and application behavior  
**Attributes**:
- `id`: Unique identifier (UUID)
- `key`: Setting key (string)
- `value`: Setting value (JSON-serializable)
- `category`: Setting category (general, recording, playback, ui, hotkeys, logging)
- `data_type`: Value type (string, integer, float, boolean, json)
- `default_value`: Default value for reset functionality
- `description`: Human-readable description of setting
- `is_advanced`: Boolean flag for advanced settings
- `modified_at`: Last modification timestamp

**Relationships**:
- Belongs to `User` (implicit single-user application)

**Validation Rules**:
- Key must be unique within category
- Value must match data type
- Category must be valid option

## Entity Relationships

```
User (implicit)
├── Has many Macros
├── Has many Hotkeys
├── Has many Schedules
├── Has many Macro Packages
└── Has many User Settings

Macro
├── Has many Actions
├── Has many Screenshots (through Actions)
├── Has many Schedules
├── Belongs to many Macro Packages
└── Has many Hotkeys (macro-specific)

Action
├── Belongs to Macro
├── Has one Screenshot
└── References Screenshot

Screenshot
├── Belongs to Action
├── Belongs to Macro
└── Stored as file or base64 data

Hotkey
├── May belong to Macro
└── References Macro (for play actions)

Schedule
├── Belongs to Macro
└── References Macro for execution

Macro Package
├── Contains many Macros
└── References Macro entities

User Settings
└── Key-value configuration storage
```

## Data Validation Rules

### Cross-Entity Validation
- Macro duration must equal sum of all action timestamps
- Screenshot count must equal action count for each macro
- Hotkey combinations must be unique across all hotkeys
- Schedule execution times must not conflict with system constraints
- Macro package must contain at least one macro

### Business Logic Validation
- Recording cannot start if another recording is active
- Playback cannot start if macro has no actions
- Hotkeys cannot be registered if system conflicts exist
- Scheduled macros cannot execute if target application is not available
- Export packages must include all referenced screenshots

## State Management

### Macro States
- **Draft**: Newly created, no actions recorded
- **Recording**: Currently capturing input events
- **Active**: Ready for playback, has recorded actions
- **Paused**: Playback paused, can be resumed
- **Playing**: Currently executing actions
- **Archived**: Marked for deletion, not accessible

### Application States
- **Idle**: No recording or playback active
- **Recording**: Capturing input events
- **Playing**: Executing macro actions
- **Editing**: Modifying macro or action properties
- **Scheduled**: Background execution of scheduled macros

## Data Persistence

### Storage Strategy
- **Primary Storage**: JSON files in user data directory
- **Backup Strategy**: Automatic backup before modifications
- **Migration Strategy**: Version-based migration for schema changes
- **Compression**: Screenshots compressed for storage efficiency

### File Organization
```
user_data/
├── macros/
│   ├── {macro_id}.json
│   └── screenshots/
│       └── {screenshot_id}.png
├── settings/
│   ├── user_settings.json
│   └── hotkeys.json
├── schedules/
│   └── {schedule_id}.json
├── packages/
│   └── {package_id}.zip
└── logs/
    ├── application.log
    └── error.log
```

---

**Data Model Status**: COMPLETE  
**All entities defined with relationships and validation rules**  
**Ready for contract generation and implementation**
