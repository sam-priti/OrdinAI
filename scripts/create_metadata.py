#!/usr/bin/env python3
"""
create_metadata.py
Scans data/raw_pdfs and data/text to create/update data/metadata.csv
Columns: doc_id,file_name,doc_type,publish_date,jurisdiction,text_path,canonical_path,source_url,checksum,notes
"""
import os, hashlib, csv
from pathlib import Path

PDF_DIR = Path("data/raw_pdfs")
TEXT_DIR = Path("data/text")
META_CSV = Path("data/metadata.csv")

def sha256_of(file_path):
    h = hashlib.sha256()
    with open(file_path,"rb") as fh:
        for chunk in iter(lambda: fh.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

existing = []
if META_CSV.exists():
    with open(META_CSV, newline='', encoding='utf-8') as f:
        existing = [row['file_name'] for row in csv.DictReader(f)]

rows = []
for pdf in PDF_DIR.glob("*.pdf"):
    fname = pdf.name
    docid = pdf.stem
    text_path = (TEXT_DIR / (pdf.stem + ".txt")).as_posix() if (TEXT_DIR / (pdf.stem + ".txt")).exists() else ""
    checksum = sha256_of(pdf)
    if fname in existing:
        continue
    rows.append({
        "doc_id": docid,
        "file_name": fname,
        "doc_type": "",
        "publish_date": "",
        "jurisdiction": "India",
        "text_path": text_path,
        "canonical_path": "",
        "source_url": "",
        "checksum": checksum,
        "notes": ""
    })

# append new rows
if rows:
    with open(META_CSV, "a", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["doc_id","file_name","doc_type","publish_date","jurisdiction","text_path","canonical_path","source_url","checksum","notes"])
        for r in rows:
            writer.writerow(r)
    print("Appended", len(rows), "rows to", META_CSV)
else:
    print("No new PDFs to add or all already indexed.")
