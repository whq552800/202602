# Childhood LRI Development-Year Peer Benchmarking

This repository provides the public code, tables, figure source data, and figure
files for the manuscript:

**Development-year peer benchmarking of childhood lower respiratory infection
burden across 203 countries and territories, 1990-2023**

## Scientific Scope

The expected burden is an SDI-year model-based benchmark referent. It is used to
separate high observed burden from benchmark-relative excess burden. Contextual
domains are descriptive post-classification profile signals and are not used as
causal attribution estimates.

## Repository Contents

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
│   └── analysis/
├── figure/
│   ├── manuscript/
│   └── SI/
├── table/
│   ├── machine_readable_source_data/
│   ├── supplementary_tables/
│   ├── data_dictionary.csv
│   └── figure_source_data_revision_v2_20260611.xlsx
├── panel0_1990_2019_direct_meteo_GBDPM_HAP_lui.csv
├── requirements.txt
└── README.md
```

The `table/` folder contains the submitted machine-readable source tables and
JAMA supplementary table CSV files. The `figure/` folder contains the final
manuscript and supplementary figure files uploaded for review. The `code/` folder
contains revision-build scripts and a lightweight validation script for the
public package.

## Machine-Readable Tables

The public table folder contains:

- 26 source-data CSV files under `table/machine_readable_source_data/`
- 9 JAMA supplementary table CSV files under `table/supplementary_tables/`
- `table/figure_source_data_revision_v2_20260611.xlsx`
- `table/data_dictionary.csv`

## Supplementary Tables

The JAMA supplementary table files are:

- `Table_S1_data_sources_indicators.csv`
- `Table_S2_expected_model_validation.csv`
- `Table_S3_annual_burden_profile_counts_2000_2023.csv`
- `Table_S4_full_2000_2023_transition_matrix.csv`
- `Table_S5_contextual_domain_definitions.csv`
- `Table_S6_country_level_contextual_lag_matrix_2000_2023.csv`
- `Table_S7_endpoint_contextual_domain_frequency_by_profile.csv`
- `Table_S8_age_boundary_sensitivity.csv`
- `Table_S9_wls_smearing_small_population_and_fixed_threshold_summary.csv`

Supplementary Table S6 is the full country-level list referenced by the main-text
Table 1 footnote. It contains 203 countries and territories and includes the 2000
and 2023 profiles, transition pathway, contextual lag-domain values, dominant
contextual lag domain, and positive lag domains.

## Key Source-Data Files

The `table/machine_readable_source_data/` folder includes the country-year
benchmark panel, 2023 profile membership, 2000-2023 transition matrices,
benchmark-residual decomposition files, contextual-domain residual files,
pathogen mortality profile files, model validation results, and robustness or
sensitivity summaries.

## Figure Files

The `figure/manuscript/` folder contains the four main manuscript figure PNG
files and the editable Illustrator file used for final layout. The `figure/SI/`
folder contains Supplementary Figures S1-S11 in PNG and PDF formats.

## Validate The Public Package

The table and figure package can be checked with:

```powershell
python code\validate_package.py
```

The validation script checks expected table files, selected table dimensions,
Supplementary Table S6 profile counts, figure source workbook integrity, and the
presence of uploaded main and supplementary figure files.

## Data Source Notes

The included files are analysis-ready derived files used for reproducibility of
the submitted supplement and figures. Original source datasets should be obtained
from the data providers under their own access and licensing terms, including
IHME/GBD, World Bank WDI, WHO GHO, ERA5, WorldPop, and Natural Earth.
