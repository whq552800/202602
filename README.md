# Childhood LRI Development-Year Peer Benchmarking

This repository provides the public code and machine-readable source-data package
for the manuscript:

**Development-year peer benchmarking of childhood lower respiratory infection
burden across 203 countries and territories, 1990-2023**

The current submitted machine-readable data package is:

```text
revision_v2_machine_readable_source_data_20260611.zip
```

SHA256:

```text
EA2817860E47E9C227D40064348F635D50A34109B0EEDA9D14A6A44312D0FC35
```

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
├── panel0_1990_2019_direct_meteo_GBDPM_HAP_lui.csv
├── requirements.txt
├── revision_v2_machine_readable_source_data_20260611.zip
└── README.md
```

The `code/` folder contains the revision-build and validation scripts used in the
local analysis environment. The submitted machine-readable tables are packaged in
the zip file above. The `figure/` folder contains the final manuscript figures
and supplementary figure files uploaded for review.

## Machine-Readable Source Data

The zip archive contains 39 files:

- 26 source-data CSV files under `machine_readable_source_data/`
- 9 JAMA supplementary table CSV files under `supplementary_tables/`
- `figure_source_data_revision_v2_20260611.xlsx`
- `data_dictionary.csv`
- `README_machine_readable_source_data_20260611.md`
- `MANIFEST_revision_v2_source_data_20260611.json`

The archive passed ZIP integrity validation (`testzip = None`) after upload.

## Supplementary Tables

The JAMA supplementary table files in the archive are:

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

The `machine_readable_source_data/` folder in the zip includes the country-year
benchmark panel, 2023 profile membership, 2000-2023 transition matrices,
benchmark-residual decomposition files, contextual-domain residual files,
pathogen mortality profile files, model validation results, and robustness or
sensitivity summaries.

## Figure Files

The `figure/manuscript/` folder contains the four main manuscript figure PNG
files and the editable Illustrator file used for final layout. The `figure/SI/`
folder contains Supplementary Figures S1-S11 in PNG and PDF formats.

## How To Inspect The Data Package

Unzip the source-data package and read the manifest and data dictionary first:

```powershell
Expand-Archive .\revision_v2_machine_readable_source_data_20260611.zip .\revision_v2_machine_readable_source_data_20260611
```

Then open:

```text
revision_v2_machine_readable_source_data_20260611\MANIFEST_revision_v2_source_data_20260611.json
revision_v2_machine_readable_source_data_20260611\data_dictionary.csv
```

## Data Source Notes

The included files are analysis-ready derived files used for reproducibility of
the submitted supplement and figures. Original source datasets should be obtained
from the data providers under their own access and licensing terms, including
IHME/GBD, World Bank WDI, WHO GHO, ERA5, WorldPop, and Natural Earth.
