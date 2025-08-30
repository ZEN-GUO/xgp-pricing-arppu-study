## [v0.2.0–data-intake] — 2025-08-29
### Added
- Pricing tables → CSV pipeline
  - Extracted Xbox pricing tables from markdown into CSV with `tools/md2csv_simple.py`.
  - Parsed outputs collected under `data/interim/parsed_tables/`.
- Country coverage & ISO2
  - Built PC Game Pass country list (85 markets) with `iso2,country,currency` → `data/processed/pc_countries_iso2_currency.csv`.
  - Produced canonical country → ISO2 mapping (normalized names) → `data/processed/country_iso2_map_filled.csv`.
  - Issued keys templates:
    - data/processed/iso2_vintage_template_2024-09-10.csv
    - data/processed/iso2_vintage_grid_2024-07-10_2024-09-10.csv
- Consolidated pricing
  - Unified wide pricing as of 2024-09-10 → `data/processed/xgp_prices_2024-09-10.csv` (user-authored, QC’d here).
- FX snapshots
  - ECB-based snapshot (USD per 1 local) → `data/processed/fx_snapshot_country_2025-08-29.csv`.
  - Google Sheets snapshot (user-sourced) 2025-08-01, validated & cleaned:
    - `data/processed/fx_snapshots_2025-08-01_checked.csv`
    - `data/processed/fx_snapshots_2025-08-01_checked_min.csv` (two columns only)
  - Filled pegged currencies with central-bank constants (AED/SAR/QAR).
  - Utility to regenerate snapshots from ECB history:
    - `tools/build_fx_snapshot_from_ecb_hist.py`
- QC
  - Ran structural and logic checks on pricing & FX:
  - key duplicates, ISO2/CCY format, `price_term`/`is_estimated_monthly` coherence,
  - monthly vs 12-month arithmetic, tier coverage vs reference lists.

### Changed
- Standardized column naming across intakes:
  - `source_vintage_date` (pricing snapshot date), `price_term` (`monthly`/`12mo`), `price_month_local` (12-month ÷ 12), upper-case `ISO2/CCY`.
- Normalized country naming (e.g., Hong Kong SAR → Hong Kong, Luxemburg → Luxembourg).

### Notes
- All pricing numbers are official-table extracts; ARPU/ARPPU remain placeholders (methods focus).
- Next: enrich Ultimate/Core/Standard availability lists, add 2025-vintage ARPU/ARPPU proxies, and compute USD-normalized price vs ARPPU gap/ratio trends over time.



## [v0.1.0-outline] — 2025-08-25
### Added
- README with FX-only method (market-level price vs ARPU/ARPPU), caveats & next steps
- `data/sample.csv` (3–5 markets × 2 tiers)
- `notebooks/01_pipeline.ipynb` with parity scatter (y=x) & league table
- `figures/parity_scatter.png`
- `requirements.txt`

### Notes
- Numbers are placeholders for demo; repo focuses on methods and reproducibility.