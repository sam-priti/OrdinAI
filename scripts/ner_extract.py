#!/usr/bin/env python3
# ner_extract.py
import json
from pathlib import Path
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 2_000_000
CANON_DIR = Path("data/canonical")
for jf in CANON_DIR.glob("*.json"):
    obj = json.loads(jf.read_text(encoding='utf-8'))
    tp = obj.get("text_path","")
    if not tp:
        continue
    text = Path(tp).read_text(encoding='utf-8', errors='ignore')
    doc = nlp(text)
    ents = []
    for e in doc.ents:
        if e.label_ in ("ORG","DATE","MONEY","PERSON","GPE"):
            ents.append({"type": e.label_, "text": e.text, "start": e.start_char, "end": e.end_char})
    obj['entities'] = ents
    jf.write_text(json.dumps(obj, indent=2), encoding='utf-8')
    print("NER done:", jf.name, "entities:", len(ents))
