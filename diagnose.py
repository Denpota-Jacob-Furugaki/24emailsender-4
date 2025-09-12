#!/usr/bin/env python3
"""
Diagnostic script to check what's wrong with the server
"""

import sys
import os

print("=== DIAGNOSTIC REPORT ===")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")

print("\n=== CHECKING IMPORTS ===")
try:
    import fastapi
    print("✓ FastAPI imported successfully")
except ImportError as e:
    print(f"✗ FastAPI import failed: {e}")

try:
    import uvicorn
    print("✓ Uvicorn imported successfully")
except ImportError as e:
    print(f"✗ Uvicorn import failed: {e}")

try:
    import jinja2
    print("✓ Jinja2 imported successfully")
except ImportError as e:
    print(f"✗ Jinja2 import failed: {e}")

try:
    import emails
    print("✓ emails module imported successfully")
except ImportError as e:
    print(f"✗ emails module import failed: {e}")

print("\n=== CHECKING MAIN MODULE ===")
try:
    from main import app
    print("✓ main.py imported successfully")
    print(f"✓ FastAPI app created: {app}")
except Exception as e:
    print(f"✗ main.py import failed: {e}")

print("\n=== CHECKING CSV FILE ===")
if os.path.exists("prospects.csv"):
    print("✓ prospects.csv exists")
    with open("prospects.csv", "r") as f:
        lines = f.readlines()
        print(f"✓ CSV has {len(lines)} lines")
else:
    print("✗ prospects.csv not found")

print("\n=== DIAGNOSTIC COMPLETE ===")
