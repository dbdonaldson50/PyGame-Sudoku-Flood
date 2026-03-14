# 🎮 Sudoku Flash

A feature-rich desktop Sudoku game with modern UI, multiple grid sizes, and advanced gameplay mechanics. Built with Python and Pygame.

**Author:** Red Donaldson  
**Version:** 2.0.0  
**Date:** March 14, 2026

---

## 🚀 Quick Start

### Run the Game

```bash
python3 sudoku_flash.py
```

Or with virtual environment:
```bash
source .venv/bin/activate
python sudoku_flash.py
```

### Installation

```bash
# Clone the repository
git clone https://github.com/dbdonaldson50/PyGame-Sudoku-Flood.git
cd PyGame-Sudoku-Flood

# Install dependencies
pip install -r requirements.txt

# Run the game
python3 sudoku_flash.py
```

---

## ✨ Features

### 🎯 Core Gameplay
- **Multiple Grid Sizes**: 9×9 (Easy), 16×16 (Medium), 25×25 (Hard)
- **Smart Auto-Fill**: Automatically fills cells with only one possible value
- **Laser Animation**: Visual cascade effect showing auto-fill progression
- **Points & Lives System**: Track your performance with scoring
- **Undo Functionality**: Revert your last move (Ctrl+Z or Cmd+Z)

### 🎨 User Interface
- **Modern Design**: Clean interface with Ubuntu Mono font
- **Hover Effects**: Cells highlight on mouse hover
- **Number Highlighting**: See all instances of a number across the grid
- **Pencil Marks**: Toggle temporary notes in cells (P key)
- **Keyboard Controls**: Full keyboard navigation and input
- **Responsive Feedback**: Visual indicators for valid/invalid moves

### ⌨️ Controls
- **Mouse**: Click cells and buttons
- **Arrow Keys**: Navigate grid
- **0-9 / Numpad**: Enter digits
- **P**: Toggle pencil mark mode
- **Delete/Backspace**: Clear cell
- **Ctrl/Cmd+Z**: Undo last move
- **Escape**: Close settings

### 🎯 Scoring System
- **Easy (9×9)**: 5 points per cell, 3 lives
- **Medium (16×16)**: 10 points per cell, 3 lives
- **Hard (25×25)**: 15 points per cell, 5 lives
- **Time Bonus**: Faster completion = more points
- **Lives Bonus**: 50 points per remaining life

---

## 📁 Project Structure

```
sudoku-game/
├── src/                      # Source code
│   ├── __init__.py
│   ├── sudoku_game.py       # Main game class and loop
│   ├── constants.py         # Configuration and constants
│   ├── game_logic.py        # Puzzle generation and validation
│   └── ui_renderer.py       # UI rendering functions
│
├── tests/                    # Test suite (134 tests, 75% coverage)
│   ├── TestResults/         # Test outputs and coverage reports
│   │   ├── htmlcov/        # HTML coverage report (generated)
│   │   ├── coverage_report.txt
│   │   ├── test_output.txt
│   │   └── final_coverage.txt
│   ├── conftest.py          # Pytest configuration
│   ├── test_game_logic.py   # Game logic tests (85 tests)
│   ├── test_constants.py    # Constants validation tests (22 tests)
│   ├── test_sudoku_game.py  # Main game tests (76 tests)
│   └── performance_test.py  # Performance benchmarks
│
├── docs/                     # Documentation
│   ├── IMPLEMENTATION_REPORT.md      # Test suite implementation details
│   ├── MAIN_MENU_REPORT.md          # Main menu feature documentation
│   ├── OPTIMIZATIONS.md             # Performance optimization details
│   ├── PERFORMANCE_REPORT.md        # 25x25 grid optimization results
│   ├── README_TESTS.md              # Testing guide
│   ├── TEST_SUMMARY.md              # Quick test reference
│   ├── SCORING_ENHANCEMENT_REPORT.md # Combo system documentation
│   ├── TEST_COVERAGE_REPORT.md      # Coverage analysis
│   ├── TEST_GUIDE.md                # Quick testing guide
│   └── QUICK_SUMMARY.md             # Executive summary
│
├── requirements.txt          # Python dependencies
├── pytest.ini               # Pytest configuration
├── run_tests.py             # Test runner script
└── README.md                # This file
```

---

## 🚀 Installation

### Requirements
- **Python 3.9+** (tested on Python 3.9.6)
- **Pygame 2.5.0+**
- **pytest 7.4.0+** (for testing)

### Setup

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # OR
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎮 Running the Game

From the project root directory:

```bash
python -m src.sudoku_game
```

Or with the virtual environment activated:

```bash
source .venv/bin/activate  # if not already activated
python -m src.sudoku_game
```

---

## 🧪 Testing

The project includes a comprehensive test suite with **58 tests** covering game logic, constants, and performance.

### Run All Tests

```bash
pytest
```

Or use the convenience script:

```bash
python run_tests.py
```

### Test Options

```bash
# Verbose output
pytest -v
python run_tests.py -v

# With coverage report
pytest --cov=src --cov-report=html
python run_tests.py -c

# Skip slow tests (performance tests)
pytest -m "not slow"
python run_tests.py --fast

# Run only slow tests
pytest -m slow
python run_tests.py --slow

# Run specific test file
pytest tests/test_game_logic.py
python run_tests.py -f tests/test_game_logic.py

# Run tests matching a name
pytest -k "auto_fill"
python run_tests.py -t auto_fill
```

### Test Coverage

- **game_logic.py**: ~95% coverage
- **constants.py**: 100% coverage
- **Total**: 58 tests (56 fast + 2 slow performance tests)

See [docs/README_TESTS.md](docs/README_TESTS.md) for detailed testing documentation.

---

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[IMPLEMENTATION_REPORT.md](docs/IMPLEMENTATION_REPORT.md)**: Test suite implementation details
- **[MAIN_MENU_REPORT.md](docs/MAIN_MENU_REPORT.md)**: Main menu screen development
- **[OPTIMIZATIONS.md](docs/OPTIMIZATIONS.md)**: Performance optimization techniques
- **[PERFORMANCE_REPORT.md](docs/PERFORMANCE_REPORT.md)**: Performance benchmarks
- **[TEST_SUMMARY.md](docs/TEST_SUMMARY.md)**: Test results summary

---

## 🎯 How to Play

1. **Select Difficulty**: Choose Easy (9×9), Medium (16×16), or Hard (25×25)
2. **Fill the Grid**: Click cells or use arrow keys to navigate
3. **Enter Numbers**: Click number buttons, type digits, or use numpad
4. **Use Pencil Marks**: Press P to toggle note-taking mode
5. **Auto-Fill**: The game automatically fills cells with only one possibility
6. **Win**: Complete the puzzle correctly before running out of lives!

### Tips
- Watch for the laser animation - it shows which cells auto-filled
- Hover over cells to see highlighting
- Use undo (Ctrl/Cmd+Z) if you make a mistake
- Pencil marks help track possibilities for harder cells

---

## 🛠️ Development

### Code Organization

- **src/constants.py**: All configuration constants (colors, fonts, difficulty settings)
- **src/game_logic.py**: Core game logic (generation, validation, auto-fill)
- **src/ui_renderer.py**: UI rendering functions (draw board, menu, animations)
- **src/sudoku_game.py**: Main game class orchestrating everything

### Key Technologies

- **Pygame**: Graphics and event handling
- **Python Standard Library**: Core game logic
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting

### Performance

- Supports up to 25×25 grids (625 cells)
- Optimized constraint propagation algorithm
- Efficient backtracking with early pruning
- See [docs/PERFORMANCE_REPORT.md](docs/PERFORMANCE_REPORT.md) for benchmarks

---

## 📝 License

This project is created by Red Donaldson for educational and entertainment purposes.

---

## 🙏 Acknowledgments

Built with:
- Python 3.9.6
- Pygame 2.5.0+
- pytest 7.4.0+
- Ubuntu Mono font

---

**Enjoy the game! 🎉**
