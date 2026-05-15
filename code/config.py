"""Path configuration for the revision/v1 LRI analysis package.

All paths are resolved relative to this file so the package can be moved as a
folder without editing hard-coded workstation directories.
"""

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DATA_ANALYSIS = PACKAGE_ROOT / "data" / "analysis"
DATA_INTERMEDIATE = PACKAGE_ROOT / "data" / "intermediate"
DATA_TABLES = PACKAGE_ROOT / "data" / "tables"
DATA_ORIGINAL_INPUTS = PACKAGE_ROOT / "data" / "original_inputs"
FIGURES = PACKAGE_ROOT / "figures"
VALIDATION = PACKAGE_ROOT / "validation"
