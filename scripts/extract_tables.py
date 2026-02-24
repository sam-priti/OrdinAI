#!/usr/bin/env python3
# extract_tables.py
from pathlib import Path
import camelot, json

RAW_DIR = Path("data/raw_pdfs")
TABLES_DIR = Path("data/tables")
TABLES_DIR.mkdir(parents=True, exist_ok=True)
CANON_DIR = Path("data/canonical")

for pdf in RAW_DIR.glob("*.pdf"):
    try:
        tables = camelot.read_pdf(str(pdf), pages='1-end')
        if tables.n > 0:
            saved = []
            for i, t in enumerate(tables):
                out = TABLES_DIR / f"{pdf.stem}_table_{i}.csv"
                t.to_csv(str(out))
                saved.append(str(out))
            # update canonical JSON if exists
            canon = CANON_DIR / (pdf.stem + ".json")
            if canon.exists():
                obj = json.loads(canon.read_text(encoding='utf-8'))
                obj['tables'] = obj.get('tables',[]) + saved
                canon.write_text(json.dumps(obj, indent=2), encoding='utf-8')
            print(f"{pdf.name}: extracted {tables.n} tables")
    except Exception as e:
        print("Table extract error", pdf.name, e)
