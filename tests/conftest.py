"""Test bootstrap for repository checkout.

Keeps `pytest` and `python -m pytest` behavior consistent even when the
editable install only packages `adaptive_odmr` and not benchmark utilities.
"""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
