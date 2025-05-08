import fitz  # PyMuPDF import 해야함
import json
from typing import List

pdf_path = "crawl5.pdf"

#pdf에서 전체 텍스트 추출
def all_text(path: str) -> str:
    temp = fitz.open(path)
    full_text = ""
    for page in temp:
        full_text += page.get_text()
    return full_text.strip()

#overlap 시키기 (20%씩)
def chunks_func(text: str, chunk_size: int = 1000, overlap_ratio: float = 0.2) -> List[str]:
    chunks = []
    overlap = int(chunk_size * overlap_ratio)
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end]
        chunks.append(chunk)
        if end == len(text):
            break
        start += chunk_size - overlap
    return chunks

full_text = all_text(pdf_path)

chunks = chunks_func(full_text, chunk_size=1000, overlap_ratio=0.2)

json_chunks = [
    {"chunkNum": i + 1, "content": chunk}
    for i, chunk in enumerate(chunks)
]

#들여쓰기 2칸으로
with open("crawl5.json", "w", encoding="utf-8") as f:
    json.dump(json_chunks, f, indent=2, ensure_ascii=False)