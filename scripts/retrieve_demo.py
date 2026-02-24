#!/usr/bin/env python3
# retrieve_demo.py
import faiss, pickle
from sentence_transformers import SentenceTransformer
import numpy as np

index = faiss.read_index("data/index/faiss_index.bin")
with open("data/index/metadata.pkl","rb") as f:
    METADATA = pickle.load(f)
with open("data/index/chunks.pkl","rb") as f:
    CHUNKS = pickle.load(f)

model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve(q, k=5):
    qv = model.encode([q]).astype('float32')
    D, I = index.search(qv, k)
    for i, idx in enumerate(I[0]):
        print(f"Rank {i+1}, score {D[0][i]:.4f}")
        print("Doc:", METADATA[idx]['file_name'])
        print("Snippet:", METADATA[idx]['snippet'][:400])
        print("---")

if __name__ == "__main__":
    queries = [
        "What does RBI say about loan classification?",
        "SEBI framework for social stock exchange",
        "auditor's opinion on going concern in annual report"
    ]
    for q in queries:
        print("=== QUERY:", q)
        retrieve(q, k=3)
