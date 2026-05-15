from __future__ import annotations

import zipfile
from pathlib import Path

from config import PACKAGE_ROOT


def check_docx(path: Path) -> None:
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f"{path} failed zip integrity at {bad}")


def main() -> None:
    for path in [
        PACKAGE_ROOT / "manuscript" / "LRI_main_manuscript_v1_english_clean.docx",
        PACKAGE_ROOT / "supplement" / "LRI_supplement_v6_submit_ready.docx",
    ]:
        check_docx(path)
        print(f"OK: {path}")


if __name__ == "__main__":
    main()
