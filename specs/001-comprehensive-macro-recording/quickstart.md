# Quickstart Guide: Macro Recording Application

**Date**: 2024-12-19  
**Branch**: `001-comprehensive-macro-recording`  
**Context**: End-to-end user workflow validation for macro recording system

## Overview
This quickstart guide validates the complete user workflow from recording a macro to playing it back with all key features working correctly.

## Prerequisites
- Windows 11 (or Windows 10 version 1903+)
- Python 3.11+ installed
- Application dependencies installed via `pip install -r requirements.txt`

## Quickstart Workflow

### 1. Application Startup
**Objective**: Verify application launches correctly with system tray integration

**Steps**:
1. Launch the application: `python main.py`
2. Verify main window appears
3. Verify system tray icon is visible
4. Right-click system tray icon to verify context menu appears
5. Test minimize to tray functionality

**Expected Results**:
- ✅ Application starts without errors
- ✅ Main window displays macro list (initially empty)
- ✅ System tray icon shows with proper context menu
- ✅ Minimize to tray works correctly
- ✅ Global hotkeys are registered (Ctrl+Shift+F9, Ctrl+Shift+F10, etc.)

### 2. Record a Simple Macro
**Objective**: Capture basic keyboard and mouse input with timing

**Steps**:
1. Click "New Macro" button or press Ctrl+Shift+F9
2. Click "Start Recording"
3. Perform these actions:
   - Click in a text field
   - Type "testuser"
   - Press Tab
   - Type "password123"
   - Press Enter
   - Wait 2 seconds
   - Click a submit button
4. Press Ctrl+Shift+F10 to stop recording
5. Enter macro name: "Test Login"

**Expected Results**:
- ✅ Recording starts immediately when hotkey pressed
- ✅ All keyboard events captured (key presses, Tab, Enter)
- ✅ Mouse clicks captured with exact coordinates
- ✅ Timing between actions preserved
- ✅ Screenshots captured for each action
- ✅ Macro appears in list with correct name and action count

### 3. Edit Macro Actions
**Objective**: Modify recorded actions and verify visual editing interface

**Steps**:
1. Double-click "Test Login" macro to open editor
2. Click on the first action in the timeline
3. Verify overlay appears showing click coordinates
4. Verify screenshot displays for that action
5. Edit the username from "testuser" to "admin"
6. Add a comment to the action: "Updated username"
7. Adjust timing of the Tab key action (increase delay by 500ms)
8. Save changes

**Expected Results**:
- ✅ Macro editor opens with timeline view
- ✅ Action overlay shows exact coordinates on screen
- ✅ Screenshot displays correctly for each action
- ✅ Text editing works for keyboard actions
- ✅ Timing adjustments work correctly
- ✅ Comments are saved and displayed
- ✅ Changes persist after save

### 4. Playback Macro
**Objective**: Execute recorded macro with precise timing

**Steps**:
1. Select "Test Login" macro from the list
2. Click "Play" button or press Ctrl+Shift+F5
3. Verify macro executes with correct timing
4. Test pause/resume functionality during playback
5. Test stop functionality
6. Verify loop playback (set loop count to 2)

**Expected Results**:
- ✅ Macro plays back with original timing preserved
- ✅ All actions execute correctly (clicks, typing, Tab, Enter)
- ✅ Pause/resume works without losing position
- ✅ Stop functionality works immediately
- ✅ Loop playback repeats correctly
- ✅ Progress indicator shows current position

### 5. Global Hotkey Testing
**Objective**: Verify system-wide hotkey functionality

**Steps**:
1. Minimize application to system tray
2. Open a text editor (Notepad)
3. Press Ctrl+Shift+F9 to start recording
4. Type some text in Notepad
5. Press Ctrl+Shift+F10 to stop recording
6. Press Ctrl+Shift+F5 to play the macro
7. Verify macro executes in Notepad even when app is minimized

**Expected Results**:
- ✅ Hotkeys work when application is minimized
- ✅ Recording starts/stops correctly from any application
- ✅ Playback executes in the currently focused application
- ✅ System tray notifications show recording/playback status

### 6. Macro Organization
**Objective**: Test macro management and search functionality

**Steps**:
1. Create 3 additional macros with different names and tags
2. Mark one macro as favorite
3. Use search function to find macros by name
4. Filter macros by tags
5. Sort macros by different criteria (name, date, duration)
6. Test macro duplication functionality

**Expected Results**:
- ✅ Multiple macros can be created and organized
- ✅ Favorite marking works correctly
- ✅ Search finds macros by name and description
- ✅ Tag filtering works correctly
- ✅ Sorting functions work for all criteria
- ✅ Duplication creates exact copy with new name

### 7. Export/Import Functionality
**Objective**: Test macro package sharing and backup

**Steps**:
1. Select multiple macros for export
2. Click "Export" and create a package file
3. Delete the original macros
4. Import the package file
5. Verify all macros are restored correctly
6. Verify screenshots are included in import

**Expected Results**:
- ✅ Export creates valid package file
- ✅ Package includes all macro data and metadata
- ✅ Screenshots are included in export
- ✅ Import restores all macros correctly
- ✅ Conflict resolution works for duplicate names
- ✅ Import validation prevents corrupted packages

### 8. Scheduling System
**Objective**: Test time-based macro execution

**Steps**:
1. Create a simple macro (type current time)
2. Set up a schedule to run every 30 seconds
3. Enable the schedule
4. Wait and verify macro executes automatically
5. Test schedule modification (change to every minute)
6. Test schedule disable/enable functionality

**Expected Results**:
- ✅ Schedule creation works correctly
- ✅ Macros execute at scheduled times
- ✅ Schedule modifications take effect immediately
- ✅ Enable/disable functionality works
- ✅ Background execution doesn't interfere with user activity

### 9. Advanced Features
**Objective**: Test advanced functionality and edge cases

**Steps**:
1. Test macro with complex timing (very fast and very slow actions)
2. Test macro with multiple monitor setup
3. Test macro with high-DPI display scaling
4. Test macro execution when target window is minimized
5. Test hotkey conflict resolution
6. Test application update notification system

**Expected Results**:
- ✅ Complex timing scenarios work correctly
- ✅ Multi-monitor setups work properly
- ✅ High-DPI scaling displays correctly
- ✅ Graceful handling of minimized windows
- ✅ Hotkey conflicts are detected and resolved
- ✅ Update notifications work correctly

### 10. Error Handling and Recovery
**Objective**: Verify robust error handling

**Steps**:
1. Test recording when target application crashes
2. Test playback when target window is closed
3. Test macro execution with insufficient permissions
4. Test application behavior during system sleep/wake
5. Test recovery from corrupted macro files
6. Test graceful shutdown during recording/playback

**Expected Results**:
- ✅ Application handles target application crashes gracefully
- ✅ Playback stops cleanly when target is unavailable
- ✅ Permission errors are handled with user notification
- ✅ System sleep/wake doesn't break functionality
- ✅ Corrupted files are detected and handled
- ✅ Graceful shutdown preserves data integrity

## Performance Validation

### Timing Accuracy
- Record a macro with precise 1-second delays
- Verify playback maintains timing within ±50ms accuracy
- Test with high-frequency input (rapid key presses)

### Memory Usage
- Monitor memory usage during long recording sessions
- Verify memory doesn't grow excessively with large macro sets
- Test with macros containing many screenshots

### System Impact
- Verify minimal CPU usage during idle state
- Test that recording doesn't impact system responsiveness
- Verify hotkey registration doesn't interfere with other applications

## Success Criteria

**Core Functionality**:
- ✅ All 10 workflow steps complete successfully
- ✅ No crashes or data loss during testing
- ✅ Performance meets specified targets (<10ms latency)
- ✅ All user stories from specification are validated

**Quality Assurance**:
- ✅ Error handling works for all edge cases
- ✅ User interface is responsive and intuitive
- ✅ System integration works correctly
- ✅ Data persistence is reliable

**User Experience**:
- ✅ Workflow is intuitive for new users
- ✅ Advanced features are discoverable
- ✅ Help and documentation are accessible
- ✅ Application feels professional and polished

---

**Quickstart Status**: READY FOR VALIDATION  
**All test scenarios defined with expected results**  
**Ready for implementation and testing**
