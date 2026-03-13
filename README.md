# Sudoku Game

A desktop Sudoku game with points and lives system, built with Python and Pygame.

## Features

- **Points System**: Earn points for each correctly placed digit
  - Easy: 5 points per cell
  - Medium: 10 points per cell
  - Hard: 15 points per cell

- **Lives System**: Limited lives per puzzle
  - Easy/Medium: 3 lives
  - Hard: 5 lives

- **Game Features**:
  - Three difficulty levels (Easy, Medium, Hard)
  - Timer to track game duration
  - Hint system (costs 10 points)
  - Solution checker
  - Bonus points for time and remaining lives

## Installation

### Requirements
- Python 3.9 or higher
- Pygame library

### Setup

1. **Clone or download this repository**

2. **Create a virtual environment (recommended)**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # OR
   .venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game

```bash
python sudoku_game.py
```

## How to Play

1. Click on an empty cell to select it
2. Click a number button (1-9) or press the number key to place it
3. Correct placements earn points; incorrect ones cost a life
4. Complete the puzzle before running out of lives!

## Scoring

- **Base Points**: Earned for each correct digit
- **Time Bonus**: Faster completion = more bonus points
- **Lives Bonus**: 50 points per remaining life

## Author

Red Donaldson - March 13, 2026
