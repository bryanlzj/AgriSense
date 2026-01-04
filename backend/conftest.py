"""
Root conftest.py to ensure proper Python path setup for tests.
"""
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))
