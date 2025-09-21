#!/usr/bin/env python3
"""
download_pdfs.py
Modes:
1) Read scripts/urls.txt (one URL per line) and download PDFs to data/raw_pdfs/
2) Scrape a single HTML page for <a href="*.pdf"> links and download them
Usage:
  python download_pdfs.py --list
  python download_pdfs.py --scrape "https://example.com/page-with-links"
"""
import requests, os, sys, argparse
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

OUT_DIR = "data/raw_pdfs"
os.makedirs(OUT_DIR, exist_ok=True)

def download(url):
    try:
        r = requests.get(url, timeout=30, stream=True)
        if r.status_code == 200 and 'application/pdf' in r.headers.get('Content-Type','').lower() or url.lower().endswith('.pdf'):
            fname = os.path.basename(urlparse(url).path) or "downloaded.pdf"
            out = os.path.join(OUT_DIR, fname)
            with open(out, "wb") as f:
                for chunk in r.iter_content(1024*1024):
                    f.write(chunk)
            print("Saved:", out)
        else:
            print("Skipping (non-pdf content-type):", url)
    except Exception as e:
        print("Error downloading", url, e)

def from_list():
    with open("scripts/urls.txt","r") as fh:
        for line in fh:
            u = line.strip()
            if u:
                download(u)

def scrape_page(page_url):
    try:
        r = requests.get(page_url, timeout=30)
        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.find_all("a", href=True)
        pdfs = []
        for a in links:
            href = a['href']
            if href.lower().endswith(".pdf"):
                pdfs.append(urljoin(page_url, href))
        pdfs = list(dict.fromkeys(pdfs))
        print(f"Found {len(pdfs)} pdf links.")
        for p in pdfs:
            download(p)
    except Exception as e:
        print("Scrape error:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="Download URLs from scripts/urls.txt")
    parser.add_argument("--scrape", type=str, help="Scrape a page for pdf links and download")
    args = parser.parse_args()
    if args.list:
        from_list()
    elif args.scrape:
        scrape_page(args.scrape)
    else:
        print("No mode specified. Use --list or --scrape")
