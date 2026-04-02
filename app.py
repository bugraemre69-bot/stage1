#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

from flask import Flask, abort, render_template

app = Flask(__name__)

CACHE_FILE = Path("data/links_cache.json")
MAX_LINKS_PER_CATEGORY = 50
REFRESH_INTERVAL = timedelta(hours=8)

CATEGORIES: dict[str, dict[str, str]] = {
    "guncel-haberler": {
        "title": "Güncel Haberler",
        "query": "makine mühendisliği haber",
    },
    "staj-programlari": {
        "title": "Staj Programları",
        "query": "makine mühendisliği staj programı",
    },
    "bitirme-projeleri": {
        "title": "Bitirme Projeleri",
        "query": "makine mühendisliği bitirme projesi",
    },
    "yarisma-programlari": {
        "title": "Yarışma Programları",
        "query": "makine mühendisliği yarışma",
    },
    "online-oturumlar": {
        "title": "Online Oturumlar",
        "query": "makine mühendisliği online seminer webinar",
    },
    "fiziksel-oturumlar": {
        "title": "Fiziksel Oturumlar",
        "query": "makine mühendisliği konferans etkinlik",
    },
}


def build_rss_url(query: str) -> str:
    return (
        "https://news.google.com/rss/search?hl=tr&gl=TR&ceid=TR:tr&q="
        f"{quote_plus(query)}"
    )


def load_cache() -> dict[str, Any]:
    if not CACHE_FILE.exists():
        return {"updated_at": None, "categories": {}}
    with CACHE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_cache(cache: dict[str, Any]) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with CACHE_FILE.open("w", encoding="utf-8") as file:
        json.dump(cache, file, ensure_ascii=False, indent=2)


def fetch_news(query: str, limit: int = MAX_LINKS_PER_CATEGORY) -> list[dict[str, str]]:
    url = build_rss_url(query)
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=15) as response:
        xml_text = response.read().decode("utf-8", errors="ignore")

    root = ET.fromstring(xml_text)
    items: list[dict[str, str]] = []
    seen_links: set[str] = set()

    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "Başlıksız bağlantı").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()

        if not link or link in seen_links:
            continue

        seen_links.add(link)
        items.append({"title": title, "url": link, "published": pub_date})

        if len(items) >= limit:
            break

    return items


def refresh_cache(force: bool = False) -> dict[str, Any]:
    cache = load_cache()
    updated_at_text = cache.get("updated_at")

    if updated_at_text and not force:
        updated_at = datetime.fromisoformat(updated_at_text)
        if datetime.now(timezone.utc) - updated_at < REFRESH_INTERVAL:
            return cache

    new_data: dict[str, Any] = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "categories": {},
    }

    for slug, meta in CATEGORIES.items():
        try:
            links = fetch_news(meta["query"], limit=MAX_LINKS_PER_CATEGORY)
            error = None
        except Exception as exc:  # noqa: BLE001
            links = cache.get("categories", {}).get(slug, {}).get("links", [])
            error = f"Bağlantılar güncellenirken hata oluştu: {exc}"

        new_data["categories"][slug] = {
            "title": meta["title"],
            "query": meta["query"],
            "links": links[:MAX_LINKS_PER_CATEGORY],
            "error": error,
        }

    save_cache(new_data)
    return new_data


@app.route("/")
def home() -> str:
    cache = refresh_cache()
    return render_template(
        "index.html",
        categories=CATEGORIES,
        updated_at=cache.get("updated_at"),
    )


@app.route("/kategori/<slug>")
def category_page(slug: str) -> str:
    if slug not in CATEGORIES:
        abort(404)

    cache = refresh_cache()
    category_data = cache.get("categories", {}).get(slug, {})

    return render_template(
        "category.html",
        categories=CATEGORIES,
        slug=slug,
        title=category_data.get("title", CATEGORIES[slug]["title"]),
        links=category_data.get("links", []),
        error=category_data.get("error"),
        updated_at=cache.get("updated_at"),
        max_links=MAX_LINKS_PER_CATEGORY,
    )


if __name__ == "__main__":
    refresh_cache(force=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
