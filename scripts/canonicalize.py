#!/usr/bin/env python3
# canonicalize.py
import csv, json, re
from pathlib import Path
from dateutil import parser as dateparser

META = Path("data/metadata.csv")
TEXT_DIR = Path("data/text")
CANON_DIR = Path("data/canonical")
CANON_DIR.mkdir(parents=True, exist_ok=True)

def guess_publish_date(text):
    # try to find first full date in doc (simple heuristic)
    dates = re.findall(r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2}|\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})\b', text)
    for d in dates:
        try:
            dt = dateparser.parse(d, fuzzy=True, dayfirst=True)
            return dt.strftime("%Y-%m-%d")
        except:
            continue
    # fallback: None
    return ""

def guess_title_and_issuer(text, fname):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    title = lines[0] if lines else fname
    issuer = ""
    # look for RBI/SEBI/MCA/BSE in first 10 lines
    for l in lines[:12]:
        if "reserve bank of india" in l.lower() or "rbi" in l[:10].lower():
            issuer = "RBI"
            break
        if "securities and exchange board" in l.lower() or "sebi" in l.lower():
            issuer = "SEBI"
            break
        if "ministry of corporate affairs" in l.lower() or "mca" in l.lower():
            issuer = "MCA"
            break
        if "bse" in l.lower():
            issuer = "BSE"
            break
    return title[:200], issuer

def main():
    rows = []
    # read metadata.csv
    with open(META, newline='', encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        rows = list(rdr)
        fieldnames = rdr.fieldnames

    updated = []
    for r in rows:
        fname = r['file_name']
        pdf_stem = Path(fname).stem
        text_path = Path(r['text_path']) if r.get('text_path') else Path("data/text") / (pdf_stem + ".txt")
        text = ""
        if text_path.exists():
            text = text_path.read_text(encoding='utf-8', errors='ignore')
        title, issuer = guess_title_and_issuer(text, fname)
        publish_date = guess_publish_date(text) or r.get('publish_date','')
        doc_type = r.get('doc_type') or ""
        if not doc_type:
            # simple heuristics
            if "circular" in title.lower() or "circular" in fname.lower():
                doc_type = "regulatory_circular"
            elif "annual report" in title.lower() or "annual report" in fname.lower() or "annual report" in pdf_stem.lower():
                doc_type = "annual_report"
            elif "notification" in title.lower() or "notification" in fname.lower():
                doc_type = "notification"
            else:
                doc_type = "unknown"

        canon = {
            "doc_id": pdf_stem,
            "file_name": fname,
            "source_url": r.get('source_url',''),
            "doc_type": doc_type,
            "publish_date": publish_date,
            "jurisdiction": r.get('jurisdiction','India'),
            "issuer": issuer,
            "text_path": str(text_path) if text_path.exists() else "",
            "tables": [],
            "entities": [],   # filled later
            "keywords": [],
            "checksum": r.get('checksum',''),
            "notes": r.get('notes','')
        }
        outp = CANON_DIR / (pdf_stem + ".json")
        outp.write_text(json.dumps(canon, indent=2), encoding='utf-8')
        # update row
        r['doc_type'] = doc_type
        r['publish_date'] = publish_date
        updated.append(r)
        print("Canonicalized:", pdf_stem)

    # write back metadata.csv (overwrite)
    with open(META, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in updated:
            writer.writerow(r)
    print("Updated metadata.csv with doc_type/publish_date where detected.")

if __name__ == "__main__":
    main()
