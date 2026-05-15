"""Refresh validation files, checksums, and the distributable v1 archive.

This maintenance script intentionally works only inside the current revision
package. It does not rebuild manuscripts from workstation-specific source
paths, so the package remains portable after being copied to another machine.
"""

from __future__ import annotations

import csv
import hashlib
import json
import zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

from config import PACKAGE_ROOT


MANUSCRIPT = PACKAGE_ROOT / "manuscript" / "LRI_main_manuscript_v1_english_clean.docx"
SUPPLEMENT = PACKAGE_ROOT / "supplement" / "LRI_supplement_v6_submit_ready.docx"
ARCHIVE = PACKAGE_ROOT.parent / "LRI_revision_v1_package_20260515.zip"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package_files() -> list[Path]:
    """Return files that should be represented in the public package."""
    files: list[Path] = []
    for path in sorted(PACKAGE_ROOT.rglob("*")):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(PACKAGE_ROOT).parts
        if "__pycache__" in relative_parts or path.suffix.lower() == ".pyc":
            continue
        files.append(path)
    return files


def inspect_docx(path: Path) -> dict[str, object]:
    """Check OOXML integrity and count core Word-package objects."""
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(path) as package:
        bad_member = package.testzip()
        document_xml = ET.fromstring(package.read("word/document.xml"))
        media = [name for name in package.namelist() if name.startswith("word/media/")]
    return {
        "path": str(path.relative_to(PACKAGE_ROOT)),
        "zip_test": bad_member,
        "paragraphs": len(document_xml.findall(".//w:p", ns)),
        "tables": len(document_xml.findall(".//w:tbl", ns)),
        "drawings": len(document_xml.findall(".//w:drawing", ns)),
        "media": len(media),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def write_validation_summary() -> Path:
    validation_dir = PACKAGE_ROOT / "validation"
    validation_dir.mkdir(exist_ok=True)
    summary = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "package_root": str(PACKAGE_ROOT),
        "manuscript": inspect_docx(MANUSCRIPT),
        "supplement": inspect_docx(SUPPLEMENT),
    }
    output = validation_dir / "docx_validation_v1.json"
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return output


def write_manifest() -> Path:
    output = PACKAGE_ROOT / "MANIFEST_sha256.csv"
    rows = []
    for path in package_files():
        rows.append(
            {
                "relative_path": str(path.relative_to(PACKAGE_ROOT)),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["relative_path", "bytes", "sha256"])
        writer.writeheader()
        writer.writerows(rows)
    return output


def write_archive() -> Path:
    if ARCHIVE.exists():
        ARCHIVE.unlink()
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in package_files():
            archive.write(path, arcname=str(Path("v1") / path.relative_to(PACKAGE_ROOT)))
    with zipfile.ZipFile(ARCHIVE) as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise RuntimeError(f"Archive integrity check failed at {bad_member}")
    return ARCHIVE


def main() -> None:
    for required in [MANUSCRIPT, SUPPLEMENT]:
        if not required.exists():
            raise FileNotFoundError(required)
    validation = write_validation_summary()
    manifest = write_manifest()
    archive = write_archive()
    print(f"Validation refreshed: {validation}")
    print(f"Manifest refreshed: {manifest}")
    print(f"Archive refreshed: {archive}")


if __name__ == "__main__":
    main()
