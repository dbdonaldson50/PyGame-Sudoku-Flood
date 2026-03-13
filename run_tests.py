#!/usr/bin/env python3
"""
Test Runner Script for Sudoku Game
Author: Red Donaldson
Date: March 13, 2026

Convenience script to run tests with common configurations.
"""

import sys
import subprocess
import argparse


def run_tests(args):
    """Run pytest with specified arguments"""
    cmd = ['pytest']
    
    if args.verbose:
        cmd.append('-v')
    
    if args.coverage:
        cmd.extend(['--cov=src', '--cov-report=html', '--cov-report=term'])
    
    if args.fast:
        cmd.extend(['-m', 'not slow'])
    
    if args.slow:
        cmd.extend(['-m', 'slow'])
    
    if args.file:
        cmd.append(args.file)
    
    if args.test:
        cmd.append(f'-k {args.test}')
    
    # Run pytest
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description='Run Sudoku Game Test Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python run_tests.py                    # Run all tests
  python run_tests.py -v                 # Verbose output
  python run_tests.py -c                 # With coverage report
  python run_tests.py --fast             # Skip slow tests
  python run_tests.py --slow             # Only slow tests
  python run_tests.py -f test_game_logic.py  # Specific file
  python run_tests.py -t auto_fill       # Tests matching name
        '''
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    parser.add_argument(
        '-c', '--coverage',
        action='store_true',
        help='Generate coverage report'
    )
    
    parser.add_argument(
        '--fast',
        action='store_true',
        help='Skip slow tests'
    )
    
    parser.add_argument(
        '--slow',
        action='store_true',
        help='Run only slow tests'
    )
    
    parser.add_argument(
        '-f', '--file',
        type=str,
        help='Run tests from specific file'
    )
    
    parser.add_argument(
        '-t', '--test',
        type=str,
        help='Run tests matching pattern'
    )
    
    args = parser.parse_args()
    
    # Validate conflicting options
    if args.fast and args.slow:
        print("Error: Cannot use --fast and --slow together")
        return 1
    
    print("=" * 60)
    print("Sudoku Game Test Suite")
    print("=" * 60)
    
    return run_tests(args)


if __name__ == '__main__':
    sys.exit(main())
