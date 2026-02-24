#!/usr/bin/env python3
# build_index.py
import json, os
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from tqdm import tqdm

CANON_DIR = Path("data/canonical")
MODEL = SentenceTransformer('all-MiniLM-L6-v2')
CHUNKS = []
METADATA = []

def chunk_text(text, max_tokens=500):
    # naive paragraph splitting
    paras = [p.strip() for p in text.split("\n\n") if len(p.strip())>30]
    out = []
    for p in paras:
        if len(p) <= 1000:
            out.append(p)
        else:
            # break long paragraphs
            for i in range(0, len(p), 800):
                out.append(p[i:i+800])
    return out

for jf in CANON_DIR.glob("*.json"):
    obj = json.loads(jf.read_text(encoding='utf-8'))
    tp = obj.get("text_path","")
    if not tp:
        continue
    text = Path(tp).read_text(encoding='utf-8', errors='ignore')
    chunks = chunk_text(text)
    for c in chunks:
        CHUNKS.append(c)
        METADATA.append({"doc_id": obj["doc_id"], "file_name": obj["file_name"], "snippet": c[:300]})

print("Total chunks:", len(CHUNKS))
embs = MODEL.encode(CHUNKS, show_progress_bar=True)
dim = embs.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embs.astype('float32'))
faiss.write_index(index, "data/index/faiss_index.bin")
# save metadata & chunks
import pickle
with open("data/index/metadata.pkl","wb") as f:
    pickle.dump(METADATA, f)
with open("data/index/chunks.pkl","wb") as f:
    pickle.dump(CHUNKS, f)
print("Index and metadata saved.")
