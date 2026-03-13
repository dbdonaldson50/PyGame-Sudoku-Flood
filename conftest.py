"""
Pytest Configuration for Sudoku Game Tests
Author: Red Donaldson
Date: March 13, 2026
"""

import pytest
import sys
import os

# Add the project root to the path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


@pytest.fixture(autouse=True)
def increase_recursion_limit():
    """Increase recursion limit for 25x25 grid generation"""
    original_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(10000)
    yield
    sys.setrecursionlimit(original_limit)


# Add any global test fixtures here if needed
