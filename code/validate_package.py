"""Validate the public revision-v2 table and figure package.

Run from the repository root:

    python code/validate_package.py

The checks use only files committed to this repository.
"""

from __future__ import annotations

import csv
import zipfile
from pathlib import Path

from config import PACKAGE_ROOT, TABLE


MACHINE_SOURCE_FILES = [
    "01_location_year_benchmark_2000_2023.csv",
    "02_profile_2023_location_level.csv",
    "03_profile_summary_2023.csv",
    "04_transition_matrix_2000_2023.csv",
    "05_transition_location_level_2000_2023.csv",
    "06_double_high_2000_decomposition.csv",
    "07_decomposition_summary_2000_double_high.csv",
    "08_full_panel_benchmark_residual_dynamics.csv",
    "09_benchmark_residual_correlation_summary.csv",
    "10_contextual_indicators_location_year.csv",
    "11_contextual_peer_residuals_2000_2023.csv",
    "12_contextual_domain_change_2000_2023.csv",
    "13_dominant_contextual_lag_domain.csv",
    "14_contextual_lag_domain_frequency.csv",
    "15_endpoint_marked_adverse_domains_2023.csv",
    "16_endpoint_marked_domain_summary_2023.csv",
    "17_pathogen_group_mortality_by_profile_2023.csv",
    "18_pathogen_specific_mortality_by_profile_2023.csv",
    "19_expected_model_validation.csv",
    "20_sensitivity_scenarios_under5.csv",
    "21_age_boundary_sensitivity.csv",
    "22_sensitivity_contextual_contrasts_under5.csv",
    "23_sensitivity_country_membership_frequency_under5.csv",
    "24_priority_threshold_sensitivity_2023.csv",
    "25_wls_overlap_sensitivity.csv",
    "26_age_boundary_cross_age_overlap.csv",
]

SUPPLEMENTARY_TABLE_FILES = [
    "Table_S1_data_sources_indicators.csv",
    "Table_S2_expected_model_validation.csv",
    "Table_S3_annual_burden_profile_counts_2000_2023.csv",
    "Table_S4_full_2000_2023_transition_matrix.csv",
    "Table_S5_contextual_domain_definitions.csv",
    "Table_S6_country_level_contextual_lag_matrix_2000_2023.csv",
    "Table_S7_endpoint_contextual_domain_frequency_by_profile.csv",
    "Table_S8_age_boundary_sensitivity.csv",
    "Table_S9_wls_smearing_small_population_and_fixed_threshold_summary.csv",
]

MAIN_FIGURES = [f"Figure-{i:02d}.png" for i in range(1, 5)]
SUPPLEMENTARY_FIGURES = [f"Supplementary_Figure_S{i:02d}" for i in range(1, 12)]


def read_csv(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def assert_exists(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(path)


def assert_csv_shape(path: Path, expected_rows: int, expected_cols: int) -> None:
    rows = read_csv(path)
    actual_rows = len(rows) - 1
    actual_cols = len(rows[0]) if rows else 0
    if (actual_rows, actual_cols) != (expected_rows, expected_cols):
        raise AssertionError(
            f"{path} shape mismatch: "
            f"expected {expected_rows} rows x {expected_cols} cols, "
            f"got {actual_rows} rows x {actual_cols} cols"
        )


def check_expected_files(base: Path, expected: list[str]) -> None:
    for name in expected:
        assert_exists(base / name)


def check_xlsx(path: Path) -> None:
    with zipfile.ZipFile(path) as package:
        bad = package.testzip()
        if bad:
            raise RuntimeError(f"{path} failed XLSX ZIP integrity at {bad}")


def check_profile_counts() -> dict[str, int]:
    path = TABLE / "supplementary_tables" / "Table_S6_country_level_contextual_lag_matrix_2000_2023.csv"
    rows = read_csv(path)
    header = rows[0]
    profile_index = header.index("Profile 2023")
    counts: dict[str, int] = {}
    for row in rows[1:]:
        counts[row[profile_index]] = counts.get(row[profile_index], 0) + 1
    expected = {
        "Double-high": 23,
        "Structural high": 45,
        "Excess-only": 45,
        "Neither": 90,
    }
    if counts != expected:
        raise AssertionError(f"Unexpected 2023 profile counts: {counts}")
    return counts


def check_figures() -> None:
    manuscript_dir = PACKAGE_ROOT / "figure" / "manuscript"
    si_dir = PACKAGE_ROOT / "figure" / "SI"
    for name in MAIN_FIGURES:
        assert_exists(manuscript_dir / name)
    assert_exists(manuscript_dir / "Figure.ai")
    for stem in SUPPLEMENTARY_FIGURES:
        png_matches = list(si_dir.glob(f"{stem}_*.png"))
        pdf_matches = list(si_dir.glob(f"{stem}_*.pdf"))
        if len(png_matches) != 1:
            raise FileNotFoundError(f"Expected one PNG for {stem}, found {len(png_matches)}")
        if len(pdf_matches) != 1:
            raise FileNotFoundError(f"Expected one PDF for {stem}, found {len(pdf_matches)}")


def main() -> None:
    source_dir = TABLE / "machine_readable_source_data"
    supp_dir = TABLE / "supplementary_tables"
    check_expected_files(source_dir, MACHINE_SOURCE_FILES)
    check_expected_files(supp_dir, SUPPLEMENTARY_TABLE_FILES)
    assert_exists(TABLE / "data_dictionary.csv")
    check_xlsx(TABLE / "figure_source_data_revision_v2_20260611.xlsx")

    assert_csv_shape(source_dir / "01_location_year_benchmark_2000_2023.csv", 4872, 16)
    assert_csv_shape(source_dir / "02_profile_2023_location_level.csv", 203, 15)
    assert_csv_shape(source_dir / "19_expected_model_validation.csv", 8, 10)
    assert_csv_shape(supp_dir / "Table_S6_country_level_contextual_lag_matrix_2000_2023.csv", 203, 16)
    profile_counts = check_profile_counts()
    check_figures()

    print("OK: public revision-v2 package validation passed")
    print(f"machine-readable source tables: {len(MACHINE_SOURCE_FILES)}")
    print(f"supplementary tables: {len(SUPPLEMENTARY_TABLE_FILES)}")
    print(f"2023 profile counts: {profile_counts}")


if __name__ == "__main__":
    main()
