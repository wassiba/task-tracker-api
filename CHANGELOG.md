# Changelog

All notable changes to the Task Tracker project are documented in this file.

---

## Version 0.4 - Drag and Drop Release

### Release Summary

This release completes the Module 3 implementation of the AI Assisted Coding course.

### Features

- Added native HTML5 drag-and-drop support.
- Implemented backend-authoritative task status updates.
- Added PATCH-based status persistence.
- Prevented duplicate drag update requests.
- Implemented drag state management and visual drop indicators.
- Added board-level error handling for drag-and-drop operations.
- Preserved modal-specific validation and server error handling.
- Maintained frontend priority sorting (High → Medium → Low → ID).
- Preserved backend enforcement of valid status transitions.

### Quality Improvements

- Improved asynchronous error handling for task refresh operations.
- Preserved backend validation messages during refresh failures.
- Distinguished PATCH failures from board refresh failures.
- Improved recovery from network interruptions.
- Preserved consistent board rendering after failed updates.

### Verification

Completed:

- Manual browser testing
- Drag-and-drop validation
- Valid transition testing
- Invalid transition testing
- Existing Create Task functionality
- Existing Edit Task functionality
- Priority sorting verification

Status:

Released as **Task Tracker v0.4**