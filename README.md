# Sudoku Game

A Sudoku game with points and lives system, available in both web (HTML/JavaScript) and desktop (Python/Tkinter) versions.

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

## Versions

### Web Version
Open `index.html` in a web browser to play.

Files:
- `index.html` - Main HTML structure
- `styles.css` - Game styling
- `script.js` - Game logic

### Desktop Version (Python/Tkinter)
Run the Python script to play:

```bash
python3 sudoku_game.py
```

Requirements:
- Python 3.x
- tkinter (usually included with Python)

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
