# 🏦 OrdinAI — Generative AI for Financial Compliance

An end-to-end data pipeline and retrieval system for processing Indian financial regulatory documents (RBI, SEBI, MCA, BSE) using NLP, semantic search, and generative AI.

---

## 📌 Features

- 📥 **PDF Downloader** — bulk download regulatory PDFs from URLs or scraped pages
- 📄 **Text Extraction** — extracts text from PDFs using pdfminer with OCR fallback (pytesseract)
- 🗂️ **Canonicalization** — converts raw documents into structured JSON with metadata
- 🏷️ **Named Entity Recognition** — extracts organizations, dates, money, and locations using spaCy
- 📊 **Table Extraction** — extracts tables from PDFs using Camelot
- 🔍 **Semantic Search** — FAISS vector index with sentence-transformers for retrieval
- 📋 **Metadata Tracking** — CSV-based metadata registry with checksums

---

## 🗂️ Project Structure

```
OrdinAI/
│
├── scripts/                          # Data pipeline scripts
│   ├── download_pdfs.py              # Download PDFs from URLs or scraped pages
│   ├── extract_text.py               # Extract text from PDFs (pdfminer + OCR)
│   ├── extract_tables.py             # Extract tables using Camelot
│   ├── canonicalize.py               # Create canonical JSON documents
│   ├── create_metadata.py            # Build/update metadata.csv
│   ├── ner_extract.py                # Named entity recognition with spaCy
│   ├── build_index.py                # Build FAISS semantic search index
│   ├── retrieve_demo.py              # Demo retrieval queries
│   └── urls.txt                      # Source URLs for documents
│
├── data/
│   ├── raw_pdfs/                     # Original downloaded PDFs
│   ├── raw_html/                     # Raw HTML pages (if scraped)
│   ├── text/                         # Extracted plain text
│   ├── canonical/                    # Canonical JSON documents
│   ├── tables/                       # Extracted tables (CSV)
│   └── index/                        # FAISS index + metadata
│
├── src/                              # Core source code (coming soon)
├── frontend/                         # UI (coming soon)
├── docker/                           # Dockerfiles (coming soon)
├── notebooks/                        # EDA and analysis notebooks
├── report/                           # Project report and slides
│
├── requirements.txt
└── .gitignore
```

---

## 🚀 Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/sam-priti/OrdinAI.git
cd OrdinAI
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**4. Run the pipeline**
```bash
# Step 1: Download PDFs
python scripts/download_pdfs.py --list

# Step 2: Extract text
python scripts/extract_text.py

# Step 3: Create metadata
python scripts/create_metadata.py

# Step 4: Canonicalize documents
python scripts/canonicalize.py

# Step 5: Extract tables
python scripts/extract_tables.py

# Step 6: Run NER
python scripts/ner_extract.py

# Step 7: Build search index
python scripts/build_index.py

# Step 8: Run demo retrieval
python scripts/retrieve_demo.py
```

---

## 📦 Requirements

```
requests
beautifulsoup4
pdfminer.six
pytesseract
pdf2image
camelot-py[cv]
spacy
sentence-transformers
faiss-cpu
numpy
tqdm
python-dateutil
```

---

## 📊 Data Sources

Regulatory documents from Indian financial authorities:

| Source | Description |
|--------|-------------|
| [RBI](https://rbi.org.in) | Reserve Bank of India — master directions, circulars |
| [SEBI](https://www.sebi.gov.in) | Securities and Exchange Board of India — circulars, frameworks |
| [BSE](https://m.bseindia.com) | Bombay Stock Exchange — notices and announcements |
| [MCA](https://www.mca.gov.in) | Ministry of Corporate Affairs — notifications |

---

## 🏷️ Document ID Convention

```
<source>_<YYYYMMDD>_<short_description>
```
Example: `rbi_20210331_know_your_customer`


---

## 📄 License

This project is for academic and educational purposes.
