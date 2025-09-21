#!/usr/bin/env python3
"""
extract_text.py
Extracts text from PDFs in data/raw_pdfs and writes data/text/<docid>.txt
Uses pdfminer for text PDFs and falls back to OCR (pytesseract + pdf2image) for scanned PDFs.
"""
import os, glob
from pathlib import Path
from pdfminer.high_level import extract_text
import pytesseract
from pdf2image import convert_from_path

RAW_DIR = "data/raw_pdfs"
OUT_DIR = "data/text"
os.makedirs(OUT_DIR, exist_ok=True)

def ocr_pdf(path):
    pages = convert_from_path(path, dpi=200)
    texts = []
    for page in pages:
        texts.append(pytesseract.image_to_string(page))
    return "\n\n".join(texts)

for pdf in Path(RAW_DIR).glob("*.pdf"):
    out_path = Path(OUT_DIR) / (pdf.stem + ".txt")
    if out_path.exists():
        print("Exists:", out_path)
        continue
    try:
        txt = extract_text(str(pdf))
        if not txt.strip() or len(txt.strip()) < 200:
            print("Using OCR for", pdf.name)
            txt = ocr_pdf(str(pdf))
        out_path.write_text(txt, encoding="utf-8")
        print("Wrote:", out_path)
    except Exception as e:
        print("Error:", pdf, e)
