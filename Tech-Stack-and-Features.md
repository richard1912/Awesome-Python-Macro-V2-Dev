# Awesome Python Macro - Tech Stack & Features

## Overview
Awesome Python Macro is a sophisticated Windows 11 desktop application for recording and replaying user input macros. It provides professional-grade automation capabilities with a modern GUI interface.

## Tech Stack

### Core Platform & Language
- **Python 3.11+** - Primary programming language
- **Windows 11** - Target platform (Windows-specific APIs required)
- **MIT License** - Open source licensing

### GUI Framework
- **PySide6 (Qt6)** - Cross-platform GUI framework for the desktop application
  - Qt Widgets - Main UI components (windows, dialogs, controls)
  - Qt Core - Event handling, signals/slots, threading
  - Qt GUI - Graphics and window management

### Input Handling & Automation
- **pynput** - Low-level input capture and simulation
- **keyboard** - Advanced keyboard input handling
- **mouse** - Mouse input capture and control
- **pywin32** - Windows-specific API access for system integration
  - win32api - Windows API functions
  - win32gui - Window management
  - win32con - Windows constants and messages

### System Integration
- **psutil** - System and process monitoring
- **Windows APIs** - Deep system integration for:
  - Global hotkey registration
  - Window focus management
  - System-wide input capture
  - Process monitoring
  - DPI awareness handling

### Data & Storage
- **JSON** - Configuration and macro data serialization
- **pathlib** - Modern file system operations
- **zipfile** - Export/import functionality for macro packages
- **Rotating file logging** - Log management with size limits

### Build & Packaging
- **PyInstaller** - Creating Windows executable (.exe)
- **setuptools** - Package management and installation
- **wheel** - Python package distribution
- **Custom build scripts** - Automated executable creation

### Development & Testing
- **pytest** - Testing framework
- **pytest-qt** - Qt-specific testing utilities
- **black** - Code formatting (88 character line length)
- **flake8** - Code linting and style checking
- **isort** - Import organization

### Additional Libraries
- **requests** - HTTP requests for update checking
- **Pillow (PIL)** - Image processing for screenshots and overlay graphics
- **logging** - Built-in Python logging with rotation
- **argparse** - Command line argument parsing
- **signal** - Process signal handling
- **threading** - Multi-threaded operations
- **ctypes** - Windows API access for overlay window management
- **datetime** - Timestamp handling for action timing

### Architecture Pattern
- **MVC-like Architecture** with clear separation of concerns:
  - **UI Layer**: Qt-based GUI components (`ui/`)
    - Main window and dialogs
    - Action overlay system
    - Screenshot display components
    - Coordinate selector interface
  - **Core Layer**: Application logic and coordination (`core/`)
  - **Storage Layer**: Data persistence and management (`storage/`)
  - **Input/Output Layer**: Recording and playback systems (`recorder/`, `player/`)
  - **Utilities Layer**: Helper functions and tools (`utils/`)
    - Screenshot capture and processing
    - Window tracking and management
    - Diagnostics and debugging tools
  - **Scheduler Layer**: Timed macro execution (`scheduler/`)
  - **Hotkeys Layer**: Global hotkey management (`hotkeys/`)
  - **Export/Import Layer**: Macro sharing and backup (`export_import/`)

## Core Features

### Macro Recording & Playback
- **Real-time Recording**: Capture keyboard and mouse input with precise timing
- **Event-based Recording**: Records individual events with exact timestamps
- **Playback Control**: Start, stop, pause, and resume macro execution
- **Timing Preservation**: Maintains original timing between actions
- **Loop Playback**: Repeat macros multiple times with configurable intervals

### Input Handling
- **Keyboard Events**: Capture and replay all keyboard inputs including:
  - Standard alphanumeric keys (A-Z, 0-9)
  - Extended function keys (F1-F24) with full Fn key support
  - Modifier keys (Ctrl, Alt, Shift, Win, Fn)
  - Special keys (Enter, Escape, Tab, Backspace, Delete, etc.)
  - Numpad keys and multimedia keys
  - International character support
- **Mouse Events**: Capture and replay mouse actions:
  - Left, right, and middle mouse clicks
  - Mouse wheel scrolling
  - Mouse movement with coordinates
  - Drag and drop operations

### Global Hotkey System
- **System-wide Hotkeys**: Register hotkeys that work across all applications
- **Comprehensive Key Support**: Support for all keyboard keys including:
  - Standard alphanumeric keys (A-Z, 0-9)
  - Function keys (F1-F24) with full Fn key support
  - Modifier keys (Ctrl, Alt, Shift, Win, Fn)
  - Special keys (Enter, Escape, Tab, Backspace, Delete, etc.)
  - Numpad keys and multimedia keys
  - Custom key combinations with multiple modifiers
- **Customizable Shortcuts**: Assign custom hotkey combinations to macros
- **Default Hotkeys**:
  - `Ctrl+Shift+F9` - Start recording
  - `Ctrl+Shift+F10` - Stop recording/playback
  - `Ctrl+Shift+F5` - Play last macro
  - `Ctrl+Shift+M` - Show/hide main window
  - `Ctrl+Shift+T` - Minimize to system tray
- **Hotkey Conflict Resolution**: Handle conflicts with existing system hotkeys
- **Hotkey Registration**: Dynamic registration and unregistration of hotkeys
- **Multi-key Combinations**: Support for complex key combinations (e.g., Ctrl+Alt+Shift+F12)

### User Interface
- **Modern GUI**: Clean, intuitive interface built with Qt6
- **Main Window**: Central control panel with macro management
- **System Tray Integration**: Complete system tray functionality including:
  - Minimize to tray option with hotkey support (`Ctrl+Shift+M`)
  - System tray icon with context menu
  - Quick access to common functions from tray
  - Tray notifications for recording/playback status
  - Right-click context menu for rapid macro access
- **Macro List**: View, search, and organize saved macros
- **Recording Controls**: Visual feedback during recording and playback
- **Settings Dialog**: Comprehensive configuration options
- **Progress Indicators**: Real-time playback progress and status
- **Action Overlay System**: Transparent overlay windows for visual action representation
- **Screenshot Integration**: Built-in screenshot capture and display capabilities

### Macro Management
- **Macro Storage**: Persistent storage of recorded macros
- **Macro Organization**: Categorize and search macros
- **Macro Editing**: Modify recorded events and timing
- **Macro Action Editor**: Advanced editing interface for individual macro actions
- **Macro Deletion**: Safe removal with confirmation dialogs
- **Macro Duplication**: Copy and modify existing macros

### Macro Action Editing
- **Visual Action Editor**: Interactive interface for editing individual macro actions
- **Action Overlay System**: When selecting macro actions, a visual overlay appears on screen showing:
  - Exact coordinates of mouse clicks
  - Visual representation of keyboard inputs
  - Timing information between actions
  - Action sequence visualization
- **Screenshot Context**: For each action, view screenshots showing:
  - The exact screen state when the action was recorded
  - Visual context of what the user was interacting with
  - Window and application state at the time of recording
  - UI elements that were targeted by the action
- **Action Modification**: Edit action properties including:
  - Mouse coordinates and click types
  - Keyboard key combinations and timing
  - Delays between actions
  - Action descriptions and notes
- **Macro Comments System**: Add descriptive comments to macros and individual actions:
  - **Macro-level Comments**: Overall description and purpose of the macro
  - **Action-level Comments**: Specific notes for individual actions
  - **Comment Display**: Comments visible in timeline and editor views
  - **Search by Comments**: Find macros by searching comment content
  - **Export Comments**: Include comments in exported macro packages
- **Visual Timeline**: Timeline view showing the sequence of actions with visual representations
- **Action Validation**: Verify that edited actions will work correctly before saving

### Export/Import System
- **Macro Packages**: Export macros as ZIP packages
- **Import Functionality**: Import macro packages from other users
- **Conflict Resolution**: Handle naming conflicts during import
- **Validation**: Verify macro integrity and compatibility
- **Sharing**: Easy sharing of macro collections

### Scheduling System
- **Scheduled Execution**: Run macros at specific times or intervals
- **Recurring Macros**: Set up macros to repeat on schedules
- **Time-based Triggers**: Execute macros based on time conditions
- **Background Execution**: Run scheduled macros without user interaction

### System Integration
- **Windows DPI Awareness**: Proper scaling on high-DPI displays
- **Administrator Privileges**: Enhanced functionality when running as admin
- **Process Monitoring**: Track and manage system processes
- **Window Management**: Focus and interact with specific applications
- **System Resource Monitoring**: Monitor CPU and memory usage

### Configuration & Settings
- **Persistent Settings**: Save user preferences and configurations
- **Default Configurations**: Sensible defaults for new users
- **Configuration Migration**: Automatic migration of settings between versions
- **Customizable Behavior**: Extensive customization options

### Update System
- **Automatic Updates**: Check for and notify about new versions
- **Manual Update Check**: User-initiated update checking
- **Version Management**: Track and manage application versions
- **Update Notifications**: Inform users about available updates

### Logging & Diagnostics
- **Comprehensive Logging**: Detailed logs for troubleshooting
- **Log Rotation**: Automatic log file management with size limits
- **Error Tracking**: Separate error logs for debugging
- **Diagnostic Tools**: Built-in diagnostic utilities
- **Event Dumping**: Export event data for analysis

### Security & Licensing
- **License Validation**: Optional license key validation system
- **License Dialog**: User-friendly license management interface
- **Security Features**: Safe execution environment
- **Permission Management**: Proper handling of system permissions

### Performance & Optimization
- **Multi-threading**: Efficient handling of concurrent operations
- **Memory Management**: Optimized memory usage for large macro sets
- **Performance Monitoring**: Track application performance
- **Resource Optimization**: Efficient system resource utilization

## Development Features

### Testing
- **Unit Tests**: Comprehensive test suite with pytest
- **GUI Tests**: Qt-specific testing with pytest-qt
- **Integration Tests**: End-to-end testing of features
- **Test Coverage**: Automated test coverage reporting

### Code Quality
- **Code Formatting**: Automated formatting with black
- **Linting**: Code quality checks with flake8
- **Import Organization**: Automated import sorting with isort
- **Type Hints**: Modern Python type annotations

### Build & Distribution
- **Executable Creation**: Single-click executable building
- **Cross-Platform Build**: Consistent build process
- **Installer Creation**: Optional installer generation
- **Distribution Scripts**: Automated release preparation

## System Requirements

### Minimum Requirements
- **OS**: Windows 10 (version 1903 or later) / Windows 11
- **Python**: 3.11 or higher
- **RAM**: 512 MB minimum
- **Storage**: 100 MB available space
- **Permissions**: User-level permissions (admin recommended)

### Recommended Requirements
- **OS**: Windows 11
- **RAM**: 2 GB or more
- **Storage**: 500 MB available space
- **Permissions**: Administrator privileges
- **Display**: High-DPI display support

## Installation & Deployment

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd awesome-python-macro

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Executable Build
```bash
# Build executable
python build_exe.py

# Build with debug console
python build_exe.py --debug

# Build single file executable
python build_exe.py --onefile
```

### Distribution
- **Standalone Executable**: No Python installation required
- **Portable Version**: Run from any location
- **Admin Script**: Batch file for elevated privileges
- **Documentation**: Included README and user guides

## Future Enhancements

### Planned Features
- **Plugin System**: Extensible architecture for custom functionality
- **Cloud Sync**: Synchronize macros across devices
- **Advanced Scheduling**: More sophisticated scheduling options
- **Macro Marketplace**: Share and discover community macros
- **Mobile Companion**: Mobile app for remote control
- **Voice Commands**: Voice-activated macro execution
- **AI Integration**: Smart macro suggestions and optimization

### Technical Improvements
- **Performance Optimization**: Further speed improvements
- **Memory Efficiency**: Reduced memory footprint
- **Cross-Platform**: Linux and macOS support
- **Web Interface**: Browser-based macro management
- **API Development**: RESTful API for external integration

---

*This document provides a comprehensive overview of the Awesome Python Macro application's technical architecture and feature set. For specific implementation details, refer to the source code and inline documentation.*
