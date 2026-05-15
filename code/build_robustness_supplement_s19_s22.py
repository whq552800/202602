"""Create submit-ready robustness tables S19-S22 for the LRI supplement.

The script uses package-local files only. Analyses that require unavailable
inputs are not written into the formal supplement.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
from config import DATA_ANALYSIS, DATA_ORIGINAL_INPUTS, PACKAGE_ROOT


OUT = PACKAGE_ROOT / "data" / "supplement_reordered"
OUT.mkdir(parents=True, exist_ok=True)


PRIMARY_HIGH = "high_observed_high_excess"
U5 = "u5"


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def write(df: pd.DataFrame, filename: str) -> Path:
    path = OUT / filename
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def classify(df: pd.DataFrame, observed_threshold: float | None = None, excess_threshold: float | None = None) -> pd.DataFrame:
    out = df.copy()
    if observed_threshold is None:
        observed_threshold = out["obs_rate"].quantile(2 / 3)
    if excess_threshold is None:
        excess_threshold = out["excess_rate"].quantile(2 / 3)
    out["high_observed_sens"] = out["obs_rate"] >= observed_threshold
    out["high_excess_sens"] = out["excess_rate"] >= excess_threshold
    out["typology_sens"] = np.select(
        [
            out["high_observed_sens"] & out["high_excess_sens"],
            out["high_observed_sens"] & ~out["high_excess_sens"],
            ~out["high_observed_sens"] & out["high_excess_sens"],
        ],
        [
            "High observed + high excess",
            "High observed, not high excess",
            "High excess, not high observed",
        ],
        default="Neither high observed nor high excess",
    )
    return out


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def profile_contrast(df: pd.DataFrame, high_set: set[str]) -> tuple[float, float]:
    """Return structural-minus-high-excess clean-cooking and HAP-PM contrasts."""
    working = df.copy()
    structural = working[working["excess_type"].eq("high_observed_not_high_excess")]
    high = working[working["iso3"].isin(high_set)]
    clean_diff = structural["clean_cooking_pct"].mean() - high["clean_cooking_pct"].mean()
    hap_diff = structural["hap_pm_pw"].mean() - high["hap_pm_pw"].mean()
    return round(clean_diff, 1), round(hap_diff, 1)


def table_s19_smearing() -> pd.DataFrame:
    pred = read_csv(DATA_ANALYSIS / "baseline_sdi_year_expected_predictions_1990_2023.csv")
    ext = read_csv(DATA_ANALYSIS / "expected_excess_classification_2023_with_external_latest_le2023.csv")
    u5_pred = pred[pred["age_group"].eq(U5)].copy()
    u5_2023 = ext[ext["age_group"].eq(U5)].copy()
    residual = np.log(u5_pred["obs_rate"]) - u5_pred["expected_log_rate"]
    smearing_factor = float(np.exp(residual).mean())

    sens = u5_2023.copy()
    sens["expected_rate"] = sens["expected_rate"] * smearing_factor
    sens["excess_rate"] = sens["obs_rate"] - sens["expected_rate"]
    sens["excess_ratio"] = sens["obs_rate"] / sens["expected_rate"]
    sens = classify(sens)
    primary_set = set(u5_2023[u5_2023["high_observed_high_excess"]]["iso3"])
    sens_set = set(sens[sens["high_observed_sens"] & sens["high_excess_sens"]]["iso3"])
    clean_diff, hap_diff = profile_contrast(u5_2023, sens_set)

    return pd.DataFrame(
        [
            {
                "model": "Duan smearing-corrected retransformation sensitivity",
                "smearing_factor": round(smearing_factor, 4),
                "n_high_observed_high_excess": len(sens_set),
                "overlap_with_primary_n": len(primary_set & sens_set),
                "jaccard_with_primary": round(jaccard(primary_set, sens_set), 3),
                "primary_only_iso3": ";".join(sorted(primary_set - sens_set)),
                "sensitivity_only_iso3": ";".join(sorted(sens_set - primary_set)),
                "clean_cooking_difference_structural_minus_high_excess": clean_diff,
                "hap_pm_difference_structural_minus_high_excess": hap_diff,
                "interpretation": "Sensitivity to log-scale retransformation; exact membership should be interpreted as threshold-sensitive.",
            }
        ]
    )


def table_s20_fixed_threshold() -> pd.DataFrame:
    data = read_csv(DATA_ANALYSIS / "country_year_sdi_context_typology_2000_2023.csv")
    base = data[data["year"].eq(2000)]
    obs_thr = float(base["obs_rate"].quantile(2 / 3))
    ex_thr = float(base["excess_rate"].quantile(2 / 3))
    rows = []
    for year, group in data.groupby("year"):
        sens = classify(group, obs_thr, ex_thr)
        counts = sens["typology_sens"].value_counts()
        rows.append(
            {
                "year": int(year),
                "observed_threshold_anchored_to_2000": obs_thr,
                "excess_threshold_anchored_to_2000": ex_thr,
                "fixed_high_observed": int(sens["high_observed_sens"].sum()),
                "fixed_high_excess": int(sens["high_excess_sens"].sum()),
                "fixed_double_high": int(counts.get("High observed + high excess", 0)),
                "fixed_high_observed_not_high_excess": int(counts.get("High observed, not high excess", 0)),
                "fixed_high_excess_not_high_observed": int(counts.get("High excess, not high observed", 0)),
                "fixed_neither": int(counts.get("Neither high observed nor high excess", 0)),
            }
        )
    return pd.DataFrame(rows).sort_values("year")


def table_s21_small_population_proxy() -> pd.DataFrame:
    ext = read_csv(DATA_ANALYSIS / "expected_excess_classification_2023_with_external_latest_le2023.csv")
    u5 = ext[ext["age_group"].eq(U5)].copy()
    primary = set(u5[u5["high_observed_high_excess"]]["iso3"])
    rows = []
    for cutoff in [500_000, 1_000_000]:
        retained = u5[u5["population_at_risk"] >= cutoff].copy()
        sens = classify(retained)
        sens_set = set(sens[sens["high_observed_sens"] & sens["high_excess_sens"]]["iso3"])
        excluded_primary = primary - set(retained["iso3"])
        clean_diff, hap_diff = profile_contrast(u5, sens_set)
        rows.append(
            {
                "exclusion_rule": f"Exclude locations with under-5 population at risk below {cutoff:,}",
                "note": "Proxy sensitivity using under-5 population at risk; total-population microstate sensitivity requires total population inputs.",
                "n_retained_locations": len(retained),
                "n_excluded_locations": len(u5) - len(retained),
                "n_high_observed_high_excess": len(sens_set),
                "overlap_with_primary_n": len(primary & sens_set),
                "jaccard_with_primary": round(jaccard(primary, sens_set), 3),
                "excluded_primary_iso3": ";".join(sorted(excluded_primary)),
                "sensitivity_only_iso3": ";".join(sorted(sens_set - primary)),
                "clean_cooking_difference_structural_minus_high_excess": clean_diff,
                "hap_pm_difference_structural_minus_high_excess": hap_diff,
            }
        )
    return pd.DataFrame(rows)


DOMAIN_MAP = {
    "Household energy": [("clean_cooking_pct", -1), ("hap_pm_pw", 1)],
    "WASH": [("basic_water_pct", -1), ("basic_sanitation_pct", -1)],
    "Immunisation/UHC": [("dpt_pct", -1), ("measles_pct", -1), ("pcv3_pct", -1), ("hib3_pct", -1), ("uhc_index", -1)],
    "HIV/TB": [("hiv_15_49_pct", 1), ("tb_incidence_per100k", 1)],
    "Nutrition": [("stunting_u5_pct", 1), ("wasting_u5_pct", 1)],
    "Health resources": [("current_health_expenditure_pc_usd", -1), ("physicians_per1000", -1), ("nurses_midwives_per1000", -1), ("hospital_beds_per1000", -1)],
}


def annual_mean_context() -> pd.DataFrame:
    wdi = read_csv(DATA_ORIGINAL_INPUTS / "worldbank_wdi_raw_2018_2024.csv")
    who = read_csv(DATA_ORIGINAL_INPUTS / "who_gho_immunisation_raw_2018_2024.csv")
    raw = pd.concat([wdi[["iso3", "indicator", "year", "value"]], who[["iso3", "indicator", "year", "value"]]], ignore_index=True)
    raw = raw[(raw["year"] >= 2018) & (raw["year"] <= 2023)]
    avg = raw.groupby(["iso3", "indicator"], as_index=False)["value"].mean()
    return avg.pivot(index="iso3", columns="indicator", values="value").reset_index()


def domain_adverse_score(df: pd.DataFrame, variables: list[tuple[str, int]]) -> pd.Series:
    vals = []
    for col, direction in variables:
        if col not in df.columns:
            continue
        series = pd.to_numeric(df[col], errors="coerce")
        if direction < 0:
            vals.append(-series)
        else:
            vals.append(series)
    if not vals:
        return pd.Series(np.nan, index=df.index)
    return pd.concat(vals, axis=1).mean(axis=1, skipna=True)


def table_s22_context_window() -> pd.DataFrame:
    ext = read_csv(DATA_ANALYSIS / "expected_excess_classification_2023_with_external_latest_le2023.csv")
    latest = ext[ext["age_group"].eq(U5)].copy()
    avg = annual_mean_context()
    window = latest.drop(columns=[c for c in avg.columns if c in latest.columns and c != "iso3"], errors="ignore").merge(avg, on="iso3", how="left")
    structural_mask = latest["excess_type"].eq("high_observed_not_high_excess")
    high_mask = latest["high_observed_high_excess"]
    rows = []
    for domain, vars_ in DOMAIN_MAP.items():
        latest_score = domain_adverse_score(latest, vars_)
        window_score = domain_adverse_score(window, vars_)
        latest_contrast = latest_score[structural_mask].mean() - latest_score[high_mask].mean()
        window_contrast = window_score[structural_mask].mean() - window_score[high_mask].mean()
        rows.append(
            {
                "domain": domain,
                "main_latest_value_contrast_structural_minus_high_excess": round(latest_contrast, 3) if pd.notna(latest_contrast) else np.nan,
                "window_2018_2023_contrast_structural_minus_high_excess": round(window_contrast, 3) if pd.notna(window_contrast) else np.nan,
                "direction_preserved": bool(np.sign(latest_contrast) == np.sign(window_contrast)) if pd.notna(latest_contrast) and pd.notna(window_contrast) else False,
                "variables_available": ";".join([col for col, _ in vars_ if col in window.columns]),
                "note": "Domain score is the mean adverse-coded raw indicator value; this is a source-year sensitivity for group profiles, not a causal ranking.",
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    for obsolete in OUT.glob("table_s2[3-9]_*.csv"):
        obsolete.unlink()
    legacy_region = OUT / "table_s21_region_aware_benchmark_sensitivity.csv"
    if legacy_region.exists():
        legacy_region.unlink()
    outputs = {
        "table_s19_duan_smearing_corrected_expected_rate_sensitivity.csv": table_s19_smearing(),
        "table_s20_2000_anchored_fixed_threshold_sensitivity.csv": table_s20_fixed_threshold(),
        "table_s21_small_population_exclusion_sensitivity.csv": table_s21_small_population_proxy(),
        "table_s22_harmonised_2018_2023_contextual_window_sensitivity.csv": table_s22_context_window(),
    }
    for filename, df in outputs.items():
        path = write(df, filename)
        print(f"Wrote {path} ({len(df)} rows)")


if __name__ == "__main__":
    main()
