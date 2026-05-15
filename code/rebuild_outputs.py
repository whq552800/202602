"""Rebuild the derived supplement tables, supplementary figures, DOCX, and archive.

Run from any working directory:

    python code/rebuild_outputs.py

The script uses only files inside the revision/v1 package.
"""

from __future__ import annotations

import os
import shutil
import zipfile
from pathlib import Path

from config import FIGURES, PACKAGE_ROOT
from build_reordered_supplement_v2 import main as build_supplement
from build_revision_v1_package import main as build_package


def remove_tree(path) -> None:
    if path.exists():
        shutil.rmtree(path)


def assert_docx_ok(path: Path) -> None:
    with zipfile.ZipFile(path) as package:
        bad = package.testzip()
        if bad:
            raise RuntimeError(f"Invalid DOCX member: {bad}")


def main() -> None:
    remove_tree(PACKAGE_ROOT / "data" / "supplement_reordered")
    remove_tree(FIGURES / "supplement")
    supplement_docx = PACKAGE_ROOT / "supplement" / "LRI_supplement_v6_submit_ready.docx"
    try:
        if supplement_docx.exists():
            supplement_docx.unlink()
        build_supplement()
        build_package()
        return
    except PermissionError:
        rebuild_dir = PACKAGE_ROOT / "validation" / "rebuild_check"
        rebuild_dir.mkdir(parents=True, exist_ok=True)
        fallback_docx = rebuild_dir / "LRI_supplement_v6_rebuilt_from_package.docx"
        os.environ["LRI_SUPPLEMENT_OUTPUT_DOCX"] = str(fallback_docx)
        build_supplement()
        assert_docx_ok(fallback_docx)
        print(f"Formal supplement was locked; wrote rebuild proof to {fallback_docx}")


if __name__ == "__main__":
    main()
