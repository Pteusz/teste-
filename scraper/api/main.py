import json
import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

OUTPUT_DIR = Path(os.environ.get("SCRAPER_OUTPUT_DIR", "/data/saidas"))

app = FastAPI(title="khoral scrap API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


def _site_file(site: str) -> Path:
    path = OUTPUT_DIR / f"{site}.jsonl"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Nenhuma raspagem encontrada para '{site}'")
    return path


def _read_items(path: Path) -> list[dict]:
    items = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


@app.get("/health")
def health():
    return {"status": "ok", "output_dir": str(OUTPUT_DIR)}


@app.get("/sites")
def list_sites():
    if not OUTPUT_DIR.is_dir():
        return []
    return sorted(p.stem for p in OUTPUT_DIR.glob("*.jsonl"))


@app.get("/sites/{site}")
def get_site_items(
    site: str,
    q: Optional[str] = Query(default=None, description="filtra por texto (case-insensitive) em qualquer campo"),
    limit: int = Query(default=100, le=1000),
    offset: int = Query(default=0, ge=0),
):
    items = _read_items(_site_file(site))

    if q:
        q_lower = q.lower()
        items = [it for it in items if q_lower in json.dumps(it, ensure_ascii=False).lower()]

    total = len(items)
    page = items[offset : offset + limit]
    return {"total": total, "count": len(page), "offset": offset, "items": page}
