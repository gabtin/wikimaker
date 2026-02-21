import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

import frontmatter

from app.config import DATA_DIR

DEFAULT_SETTINGS = {
    "purpose": "personal_reference",       # personal_reference | study_guide | research_map | explain_to_others
    "granularity": "standard",             # broad | standard | fine
    "voice_preservation": "medium",        # low | medium | high
    "page_depth": "standard",              # brief | standard | comprehensive
    "critical_lens": "descriptive",        # descriptive | analytical | critical
    "focus_areas": "",                     # free-text comma-separated tags
    "link_density": "moderate",            # minimal | moderate | dense
}


def slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def author_dir(author_slug: str) -> Path:
    return DATA_DIR / author_slug


def get_author_meta(author_slug: str) -> dict:
    meta_path = author_dir(author_slug) / "meta.json"
    if not meta_path.exists():
        return {}
    return json.loads(meta_path.read_text())


def save_author_meta(author_slug: str, meta: dict):
    d = author_dir(author_slug)
    d.mkdir(parents=True, exist_ok=True)
    (d / "meta.json").write_text(json.dumps(meta, indent=2))


def create_author(name: str) -> str:
    """Create a new author wiki. Returns the slug."""
    slug = slugify(name)
    d = author_dir(slug)
    d.mkdir(parents=True, exist_ok=True)
    (d / "_sources").mkdir(exist_ok=True)
    (d / "concepts").mkdir(exist_ok=True)
    meta = {
        "name": name,
        "slug": slug,
        "sources": [],
        "settings": dict(DEFAULT_SETTINGS),
        "created": datetime.now(timezone.utc).isoformat(),
    }
    save_author_meta(slug, meta)
    return slug


def list_authors() -> list[dict]:
    """Return list of all author metadata dicts."""
    if not DATA_DIR.exists():
        return []
    authors = []
    for d in sorted(DATA_DIR.iterdir()):
        if d.is_dir():
            meta = get_author_meta(d.name)
            if meta:
                authors.append(meta)
    return authors


def save_source(author_slug: str, text: str, source_hash: str, source_label: str):
    """Save raw source text and record it in author meta."""
    src_dir = author_dir(author_slug) / "_sources"
    src_dir.mkdir(parents=True, exist_ok=True)
    (src_dir / f"{source_hash}.txt").write_text(text)

    meta = get_author_meta(author_slug)
    meta.setdefault("sources", []).append({
        "label": source_label,
        "hash": source_hash,
        "added": datetime.now(timezone.utc).isoformat(),
    })
    save_author_meta(author_slug, meta)


def list_concepts(author_slug: str) -> list[dict]:
    """List all concept pages for an author (title + slug from frontmatter)."""
    concepts_dir = author_dir(author_slug) / "concepts"
    if not concepts_dir.exists():
        return []
    concepts = []
    for f in sorted(concepts_dir.glob("*.md")):
        post = frontmatter.load(str(f))
        concepts.append({
            "slug": f.stem,
            "title": post.metadata.get("title", f.stem),
            "sources": post.metadata.get("sources", []),
            "last_updated": post.metadata.get("last_updated", ""),
            "tags": post.metadata.get("tags", []),
        })
    return concepts


def list_all_tags(author_slug: str) -> list[str]:
    """Collect unique tags across all concepts for an author, sorted."""
    tags = set()
    for c in list_concepts(author_slug):
        tags.update(c.get("tags", []))
    return sorted(tags)


def read_concept(author_slug: str, concept_slug: str) -> frontmatter.Post | None:
    """Read a concept page. Returns frontmatter Post or None."""
    path = author_dir(author_slug) / "concepts" / f"{concept_slug}.md"
    if not path.exists():
        return None
    return frontmatter.load(str(path))


def write_concept(author_slug: str, concept_slug: str, title: str, content: str,
                  sources: list[str], extra_meta: dict | None = None):
    """Write a concept page with YAML frontmatter."""
    concepts_dir = author_dir(author_slug) / "concepts"
    concepts_dir.mkdir(parents=True, exist_ok=True)

    metadata = {
        "title": title,
        "author": author_slug,
        "sources": sources,
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }
    if extra_meta:
        metadata.update(extra_meta)

    post = frontmatter.Post(content, **metadata)
    path = concepts_dir / f"{concept_slug}.md"
    path.write_text(frontmatter.dumps(post))


def concept_exists(author_slug: str, concept_slug: str) -> bool:
    return (author_dir(author_slug) / "concepts" / f"{concept_slug}.md").exists()


def get_settings(author_slug: str) -> dict:
    """Get wiki settings, filling in defaults for any missing keys."""
    meta = get_author_meta(author_slug)
    saved = meta.get("settings", {})
    return {**DEFAULT_SETTINGS, **saved}


def save_settings(author_slug: str, settings: dict):
    """Update wiki settings in author meta."""
    meta = get_author_meta(author_slug)
    meta["settings"] = {**DEFAULT_SETTINGS, **settings}
    save_author_meta(author_slug, meta)


def delete_concept(author_slug: str, concept_slug: str):
    """Delete a single concept page."""
    path = author_dir(author_slug) / "concepts" / f"{concept_slug}.md"
    if path.exists():
        path.unlink()


def delete_author(author_slug: str):
    """Delete an author wiki and all its data."""
    d = author_dir(author_slug)
    if d.exists():
        shutil.rmtree(d)
