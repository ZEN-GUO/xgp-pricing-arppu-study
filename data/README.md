data/
  raw/
    # Original source artifacts (PDF/MD) for pricing tables.
  interim/
    # Working markdown tables + parser outputs
    parsed_tables/
      # CSVs extracted from each MD table
  processed/
    xgp_prices_2024-09-10.csv                 # unified pricing (wide → long, normalized)
    fx_snapshots_2025-08-01.csv               # fx data from google finical

Data acquisition (pricing)
- Primary: Official Xbox pricing tables (PDF/MD) for:
- Game Pass Standard (pricing list, 2024-09-10 vintage)
- Game Pass Ultimate/Core (price-change lists, effective 2024-07-10)
- PC Game Pass (pricing list with availability)
- Method: save original files under `data/raw/`, convert tabular content to markdown (if needed), then to CSV via `tools/md2csv.py`.

Markdown → CSV
- Script: tools/md2csv_simple.py
- What it does:
  - Parses HTML/pipe tables in .md → emits parsed_tables/*.csv (adds source_vintage_date if the filename contains YYYY-MM-DD).
- Usage:
pip install pandas lxml
# Convert all MD tables in an interim folder
python tools/md2csv_simple.py data/interim
# Or specific files
python tools/md2csv_simple.py data/interim/xgp_standard_pricing_table_2024-09-10.md

FX data
- Google Sheets (GOOGLEFINANCE) — used for 2025-08-01 file
- Orientation: we need USD per 1 local. For GoogleFinance, `=INDEX(GOOGLEFINANCE("CURRENCY:" & <LOCAL> & "USD", "price", DATE(2025,8,1)), 2, 2)`.
- Export the range as CSV → save under data/processed/fx_snapshots_YYYY-MM-DD.csv.
