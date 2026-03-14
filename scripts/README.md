# Development Scripts

This directory contains diagnostic, demonstration, and verification scripts for the Sudoku Flash game.

## Scripts Overview

### Verification & Testing
- **`verify_symmetry.py`** - Automated verification that puzzle generation creates symmetric patterns
- **`smoke_test_symmetry.py`** - End-to-end smoke test for symmetry across all difficulty levels
- **`verify_modal_visual.py`** - Visual verification tool for the remaining digits modal

### Demonstrations
- **`demo_symmetry.py`** - Visual demonstration of puzzle symmetry with side-by-side comparison

### Diagnostics
- **`diagnostic_remaining_modal.py`** - Diagnostic tool for debugging remaining digits modal issues
- **`inspect_layout.py`** - Layout inspection tool for verifying button positioning and UI elements

## Usage

Run any script directly from the project root:

```bash
# Verify puzzle symmetry
python scripts/verify_symmetry.py

# Run smoke test
python scripts/smoke_test_symmetry.py

# Visual demos
python scripts/demo_symmetry.py
python scripts/verify_modal_visual.py
```

## Notes

These scripts are for development and debugging purposes. They are not required for normal gameplay.
