#!/usr/bin/env python3
"""
Sudoku Game Launcher
Author: Red Donaldson
Date: March 13, 2026

Launches the Sudoku web game using Python's built-in HTTP server.
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path


def main():
    """Launch the Sudoku game in the default web browser"""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.resolve()
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Check if index.html exists
    if not Path('index.html').exists():
        print("Error: index.html not found in the current directory!")
        sys.exit(1)
    
    # Port to run the server on
    PORT = 8000
    
    # Create server
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Try to find an available port
    for port in range(PORT, PORT + 10):
        try:
            with socketserver.TCPServer(("", port), Handler) as httpd:
                print(f"🎮 Sudoku Game Server Starting...")
                print(f"📡 Server running at: http://localhost:{port}")
                print(f"🌐 Opening game in your browser...")
                print(f"\n⌨️  Press Ctrl+C to stop the server\n")
                
                # Open the browser
                webbrowser.open(f'http://localhost:{port}/index.html')
                
                # Start serving
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\n\n👋 Server stopped. Thanks for playing!")
                    sys.exit(0)
        except OSError:
            continue
    
    print(f"Error: Could not find an available port between {PORT} and {PORT + 10}")
    sys.exit(1)


if __name__ == "__main__":
    main()
