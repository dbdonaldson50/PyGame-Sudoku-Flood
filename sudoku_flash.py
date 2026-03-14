#!/usr/bin/env python3
"""
Sudoku Flash Game Launcher
Author: Red Donaldson
Date: March 14, 2026

Run this script to start the game.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the game
from sudoku_game import SudokuGame

if __name__ == '__main__':
    game = SudokuGame()
    game.run()
