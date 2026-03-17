#!/usr/bin/env python3
"""
run_all.py (DEPRECATED) - Backwards compatibility shim.

This file was replaced by `run_SLRanalytics.py` (comments translated to English).
To preserve backwards compatibility, this script simply runs `run_SLRanalytics.py`.
"""

from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parent

print("This file (run_all.py) has been replaced by run_SLRanalytics.py.")
print("Running run_SLRanalytics.py for backward compatibility...\n")
runpy.run_path(str(ROOT / "run_SLRanalytics.py"), run_name="__main__")
