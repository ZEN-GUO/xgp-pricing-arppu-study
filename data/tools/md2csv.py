
import sys, re
from pathlib import Path
import pandas as pd

def extract_date(stem: str):
    m = re.search(r'(20\d{2})[-_](0[1-9]|1[0-2])[-_](0[1-9]|[12]\d|3[01])', stem)
    return None if not m else f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

def parse_pipe_tables(md_text: str):
    # Minimal pipe table parser (header |---| line, then rows until blank/non-pipe).
    lines = md_text.splitlines()
    tables = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if '|' in line:
            header = line.strip()
            if i + 1 < len(lines):
                delim = lines[i+1].strip()
                if '|' in delim and ('---' in delim or '---:' in delim or ':---' in delim):
                    def split_row(s):
                        cells = [c.strip() for c in s.strip().split('|')]
                        if cells and cells[0] == '': cells = cells[1:]
                        if cells and cells[-1] == '': cells = cells[:-1]
                        return cells
                    h = split_row(header)
                    d = split_row(delim)
                    if len(h) == len(d) and len(h) > 0:
                        rows = []
                        j = i + 2
                        while j < len(lines) and '|' in lines[j]:
                            r = split_row(lines[j].strip())
                            if len(r) < len(h): r += [''] * (len(h) - len(r))
                            elif len(r) > len(h): r = r[:len(h)]
                            rows.append(r)
                            j += 1
                        tables.append(pd.DataFrame(rows, columns=h))
                        i = j
                        continue
        i += 1
    return tables

def md_to_csv(md_path: Path, outdir: Path):
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    date = extract_date(md_path.stem)
    outdir.mkdir(parents=True, exist_ok=True)

    # 1) Try HTML <table> first
    tables = []
    try:
        tables = pd.read_html(text)  # needs lxml installed
    except Exception:
        tables = []

    # 2) Fallback to pipe tables if no HTML tables found
    if not tables:
        try:
            tables = parse_pipe_tables(text)
        except Exception:
            tables = []

    if not tables:
        print(f"[skip] no tables in {md_path.name}")
        return []

    created = []
    for i, df in enumerate(tables, 1):
        # Clean whitespace
        for c in df.columns:
            if df[c].dtype == object:
                df[c] = df[c].astype(str).str.replace("\u00a0", " ").str.strip()
        if date:
            df["source_vintage_date"] = date
        out = outdir / f"{md_path.stem}.table{i}.csv"
        df.to_csv(out, index=False, encoding="utf-8")
        print(f"[ok] {out}")
        created.append(str(out))
    return created

def main():
    args = sys.argv[1:] or ['.']
    # Discover .md files from args (files or dirs)
    md_files = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            md_files += sorted(p.glob("*.md"))
        elif p.is_file() and p.suffix.lower() == ".md":
            md_files.append(p)
    if not md_files:
        print("No markdown files found.")
        return
    outdir = Path("parsed_tables")
    for md in md_files:
        md_to_csv(md, outdir)

if __name__ == "__main__":
    main()
