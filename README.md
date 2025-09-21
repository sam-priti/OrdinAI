# OrdinAI - Data collection
Project: OrdinAI - Generative AI for Financial Compliance
Folders:
- data/raw_pdfs: original PDFs
- data/raw_html: raw HTML pages if scraped
- data/text: extracted text
- data/canonical: canonical JSON documents
- data/tables: extracted tables (CSV)
- data/index: local indexes (faiss)
- scripts: helper scripts (download, extract, canonicalize)
- notebooks: jupyter notebooks for EDA
- report: project report and slides
  
## Naming Conventions & doc_id Policy

- **doc_id**: `<source>_<YYYYMMDD>_<short>` (e.g., `rbi_20210331_know_your_customer`)
- **File names**: Preserve original where possible. Canonical JSON filenames: `<doc_id>.json`.
- **publish_date**: Use ISO format `YYYY-MM-DD`.
