# Childhood LRI Development-Conditioned Typology Analysis

This repository contains the code and package-local analysis files used to reproduce the supplementary tables and figures for the childhood lower respiratory infection (LRI) development-conditioned observed/excess typology analysis, 1990-2023.

The repository is organised for peer-review audit. It focuses on rebuilding the submitted supplementary materials from the included analysis-ready files. It is not a causal attribution pipeline.

## Interpretation Boundary

The expected burden is an SDI-year model-based benchmark referent. It should not be interpreted as:

- a causal counterfactual
- a frontier minimum
- an avoidable or preventable burden estimate
- an attributable burden estimate

Contextual residual fingerprints are descriptive post-classification profiles for hypothesis generation. They should not be interpreted as causal drivers or ranked attributable contributors.

## Repository Structure

```text
.
├── code/
│   ├── config.py
│   ├── rebuild_outputs.py
│   ├── build_reordered_supplement_v2.py
│   ├── build_robustness_supplement_s19_s22.py
│   ├── build_supplementary_figures.py
│   ├── build_revision_v1_package.py
│   └── validate_package.py
├── data/
│   ├── analysis/
│   ├── intermediate/
│   ├── original_inputs/
│   ├── tables/
│   └── supplement_reordered/
├── figures/
│   └── supplement/
├── README.md
├── requirements.txt
└── .gitignore
```

## Directory Guide

- `code/`: portable Python scripts. Paths are resolved relative to the repository root.
- `data/analysis/`: analysis-ready country-year files and benchmark-model outputs used by the robustness checks and supplement builders.
- `data/intermediate/`: neutral-named pathway intermediate files used to rebuild Supplementary Tables S6-S8.
- `data/original_inputs/`: WDI and WHO GHO extracts used for the 2018-2023 contextual-window sensitivity.
- `data/tables/`: cleaned source tables used by `build_reordered_supplement_v2.py`. Some filenames preserve historical working names and are not final supplementary table numbers.
- `data/supplement_reordered/`: final machine-readable Supplementary Tables S1-S22.
- `figures/supplement/`: generated Supplementary Figures S1-S3.

## Quick Start

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Rebuild supplementary tables, supplementary figures, and validation outputs:

```bash
python code/rebuild_outputs.py
```

On Windows PowerShell, the equivalent command is:

```powershell
python code\rebuild_outputs.py
```

## Expected Outputs

A successful rebuild should produce or refresh:

- `data/supplement_reordered/table_s1_*.csv` through `table_s22_*.csv`
- `figures/supplement/supplementary_figure_s1_*.png` through `supplementary_figure_s3_*.png`
- package validation metadata and manifest files, if the optional output directories are present

If the formal supplementary appendix DOCX is present in a local review package and is locked by Word, `rebuild_outputs.py` writes a rebuild proof to `validation/rebuild_check/`.

## Main Scripts

- `code/config.py`: central path configuration.
- `code/rebuild_outputs.py`: one-command rebuild of derived outputs.
- `code/build_reordered_supplement_v2.py`: rebuilds the reordered Supplementary Appendix and machine-readable Supplementary Tables S1-S22 when the DOCX output directory is available.
- `code/build_robustness_supplement_s19_s22.py`: rebuilds robustness Tables S19-S22.
- `code/build_supplementary_figures.py`: rebuilds Supplementary Figures S1-S3.
- `code/build_revision_v1_package.py`: refreshes package validation metadata, manifest, and zip archive in the full local review package.
- `code/validate_package.py`: checks DOCX files as valid OOXML zip packages in the full local review package.

## Robustness Analyses Implemented

The included code and data support:

- Duan smearing-corrected expected-rate sensitivity.
- 2000-anchored fixed-threshold sensitivity.
- Small-population exclusion sensitivity using available under-5 population-at-risk.
- Harmonised 2018-2023 contextual-window sensitivity.
- Threshold and excess-rule sensitivity.
- Profile contrast stability.
- Expected-burden model validation.
- Population-weighted WLS sensitivity.
- Age-boundary and cross-age overlap summaries.

## Analyses Not Implemented Or Claimed

This repository does not estimate:

- GBD super-region fixed-effect sensitivity
- Moran's I spatial-autocorrelation diagnostics
- Bayesian spatial models
- posterior exceedance classification
- prediction-interval classification

These analyses were not performed because the revision package did not include posterior draws, a documented GBD super-region hierarchy, or country geometry/centroid crosswalks.

## Data Source Notes

The included files are analysis-ready and derived files used for reproducibility of the submitted supplement. Original source datasets should be obtained from the data providers under their own access and licensing terms, including IHME/GBD, World Bank WDI, WHO GHO, ERA5, WorldPop, and Natural Earth.

Supplementary Table S1 documents data sources, variable definitions, source fields, and processing rules.
