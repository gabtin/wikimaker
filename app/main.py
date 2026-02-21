import logging
import re

import markdown
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.ingestion.scraper import scrape_url, hash_text, is_publication_url, discover_articles
from app.ingestion.text import clean_text
from app.ingestion.youtube import fetch_youtube_transcript
from app.processing.extractor import extract_concepts
from app.processing.merger import generate_page
from app.processing.linker import link_concepts
from app.processing.prompts import tagging_instructions
from app.storage.wiki import (
    list_authors, create_author, get_author_meta,
    save_source, list_concepts, read_concept, write_concept,
    delete_author, delete_concept, slugify,
    get_settings, save_settings, list_all_tags,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="WikiMaker")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


def render_wiki_links(html: str, author_slug: str, concept_titles: list[str]) -> str:
    """Convert [[wiki-links]] in HTML to clickable <a> tags."""
    from app.storage.wiki import slugify

    def replace_link(match):
        title = match.group(1)
        slug = slugify(title)
        return f'<a href="/{author_slug}/{slug}">{title}</a>'

    return re.sub(r"\[\[(.+?)\]\]", replace_link, html)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    authors = list_authors()
    return templates.TemplateResponse("home.html", {
        "request": request,
        "authors": authors,
    })


@app.post("/create")
async def create_wiki(author_name: str = Form(...)):
    slug = create_author(author_name)
    return RedirectResponse(url=f"/{slug}/", status_code=303)


@app.post("/{author_slug}/delete")
async def delete_wiki(author_slug: str):
    delete_author(author_slug)
    return RedirectResponse(url="/", status_code=303)


@app.get("/{author_slug}/settings", response_class=HTMLResponse)
async def settings_page(request: Request, author_slug: str):
    meta = get_author_meta(author_slug)
    if not meta:
        return RedirectResponse(url="/")
    settings = get_settings(author_slug)

    # Pass settings as an object with attribute access for the template
    class S:
        def __init__(self, d):
            self.__dict__.update(d)

    return templates.TemplateResponse("settings.html", {
        "request": request,
        "meta": meta,
        "settings": S(settings),
    })


@app.post("/{author_slug}/settings")
async def save_settings_route(
    request: Request,
    author_slug: str,
    purpose: str = Form(...),
    granularity: str = Form(...),
    voice_preservation: str = Form(...),
    page_depth: str = Form(...),
    critical_lens: str = Form(...),
    focus_areas: str = Form(""),
    link_density: str = Form(...),
):
    save_settings(author_slug, {
        "purpose": purpose,
        "granularity": granularity,
        "voice_preservation": voice_preservation,
        "page_depth": page_depth,
        "critical_lens": critical_lens,
        "focus_areas": focus_areas,
        "link_density": link_density,
    })
    return RedirectResponse(url=f"/{author_slug}/", status_code=303)


@app.get("/{author_slug}/", response_class=HTMLResponse)
async def author_page(request: Request, author_slug: str):
    meta = get_author_meta(author_slug)
    if not meta:
        return RedirectResponse(url="/")
    concepts = list_concepts(author_slug)
    all_tags = list_all_tags(author_slug)
    return templates.TemplateResponse("author.html", {
        "request": request,
        "meta": meta,
        "concepts": concepts,
        "all_tags": all_tags,
    })


@app.get("/{author_slug}/add", response_class=HTMLResponse)
async def add_source_form(request: Request, author_slug: str):
    meta = get_author_meta(author_slug)
    if not meta:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("add_source.html", {
        "request": request,
        "meta": meta,
    })


@app.post("/{author_slug}/add", response_class=HTMLResponse)
async def add_source(
    request: Request,
    author_slug: str,
    source_type: str = Form(...),
    url: str = Form(None),
    youtube_url: str = Form(None),
    raw_text: str = Form(None),
    text_label: str = Form(None),
):
    meta = get_author_meta(author_slug)
    if not meta:
        return HTMLResponse("<p>Author not found.</p>", status_code=404)

    author_name = meta["name"]
    settings = get_settings(author_slug)

    # 1. Ingest — detect publication vs single article
    try:
        if source_type == "url" and url:
            if is_publication_url(url):
                return await _process_publication(url, author_slug, author_name, settings)
            text = scrape_url(url)
            source_label = url
        elif source_type == "youtube" and youtube_url:
            text = fetch_youtube_transcript(youtube_url)
            source_label = youtube_url
        elif source_type == "text" and raw_text:
            text = clean_text(raw_text)
            source_label = text_label or "Pasted text"
        else:
            return HTMLResponse("<p>Please provide a URL or text.</p>", status_code=400)
    except ValueError as e:
        return HTMLResponse(f"<p>Error: {e}</p>", status_code=400)

    total_concepts = await _process_single_source(text, source_label, author_slug, author_name, settings)

    return HTMLResponse(
        f'<div class="processing-msg">'
        f'Done! Extracted {total_concepts} concept{"s" if total_concepts != 1 else ""}. '
        f'<a href="/{author_slug}/">View wiki &rarr;</a>'
        f'</div>'
    )


async def _process_single_source(text: str, source_label: str, author_slug: str,
                                  author_name: str, settings: dict) -> int:
    """Process one source text through the full pipeline. Returns concept count."""
    source_hash = hash_text(text)
    save_source(author_slug, text, source_hash, source_label)

    # Pass existing concept titles so extractor can match/merge
    existing_titles = [c["title"] for c in list_concepts(author_slug)]

    concepts = await extract_concepts(text, author_name, settings, existing_titles)
    if not concepts:
        return 0

    for concept in concepts:
        await generate_page(concept, author_name, author_slug, source_label, settings)

    await link_concepts(author_slug, author_name, settings)
    return len(concepts)


async def _process_publication(url: str, author_slug: str, author_name: str,
                               settings: dict) -> HTMLResponse:
    """Discover articles from a publication URL and process each one."""
    try:
        articles = discover_articles(url, max_articles=10)
    except ValueError as e:
        return HTMLResponse(f"<p>Error: {e}</p>", status_code=400)

    total_concepts = 0
    articles_processed = 0

    for article in articles:
        try:
            text = scrape_url(article["url"])
        except ValueError:
            logger.warning("Failed to scrape article: %s", article["url"])
            continue

        label = article.get("title") or article["url"]
        count = await _process_single_source(text, label, author_slug, author_name, settings)
        total_concepts += count
        articles_processed += 1
        logger.info("Processed article %d/%d: %s (%d concepts)",
                     articles_processed, len(articles), label, count)

    return HTMLResponse(
        f'<div class="processing-msg">'
        f'Done! Processed {articles_processed} article{"s" if articles_processed != 1 else ""}, '
        f'extracted {total_concepts} concept{"s" if total_concepts != 1 else ""}. '
        f'<a href="/{author_slug}/">View wiki &rarr;</a>'
        f'</div>'
    )


@app.get("/{author_slug}/search", response_class=HTMLResponse)
async def search_page(request: Request, author_slug: str, q: str = "", tag: str = ""):
    meta = get_author_meta(author_slug)
    if not meta:
        return RedirectResponse(url="/")

    concepts = list_concepts(author_slug)
    all_tags = list_all_tags(author_slug)
    results = []

    # Filter by tag first
    if tag:
        concepts = [c for c in concepts if tag in c.get("tags", [])]

    if q or tag:
        q_lower = q.lower()
        for c in concepts:
            score = 0
            if q_lower:
                if q_lower in c["title"].lower():
                    score += 3
                if any(q_lower in t for t in c.get("tags", [])):
                    score += 2
                # Read body content for text search
                post = read_concept(author_slug, c["slug"])
                if post and q_lower in post.content.lower():
                    score += 1
            else:
                # tag-only filter, all matching concepts get score 1
                score = 1
            if score > 0:
                results.append({**c, "score": score})
        results.sort(key=lambda x: x["score"], reverse=True)

    return templates.TemplateResponse("search_results.html", {
        "request": request,
        "meta": meta,
        "q": q,
        "active_tag": tag,
        "all_tags": all_tags,
        "results": results,
    })


@app.post("/{author_slug}/retag")
async def retag_all(author_slug: str):
    from app.processing.llm import chat
    import json

    meta = get_author_meta(author_slug)
    if not meta:
        return RedirectResponse(url="/", status_code=303)

    concepts = list_concepts(author_slug)
    for c in concepts:
        post = read_concept(author_slug, c["slug"])
        if not post:
            continue
        prompt = tagging_instructions(c["title"], post.content)
        response = await chat([{"role": "user", "content": prompt}])
        try:
            response = response.strip()
            if response.startswith("```"):
                lines = response.split("\n")
                lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                response = "\n".join(lines)
            tags = json.loads(response)
            if isinstance(tags, list):
                tags = [t for t in tags if isinstance(t, str)]
                write_concept(
                    author_slug=author_slug,
                    concept_slug=c["slug"],
                    title=c["title"],
                    content=post.content,
                    sources=post.metadata.get("sources", []),
                    extra_meta={"tags": sorted(set(tags))},
                )
        except (json.JSONDecodeError, ValueError):
            logger.warning("Failed to retag concept: %s", c["slug"])
            continue

    return RedirectResponse(url=f"/{author_slug}/", status_code=303)


@app.get("/{author_slug}/edit/{concept_slug}", response_class=HTMLResponse)
async def edit_concept_form(request: Request, author_slug: str, concept_slug: str):
    meta = get_author_meta(author_slug)
    if not meta:
        return RedirectResponse(url="/")
    post = read_concept(author_slug, concept_slug)
    if not post:
        return RedirectResponse(url=f"/{author_slug}/")
    return templates.TemplateResponse("edit_concept.html", {
        "request": request,
        "author_slug": author_slug,
        "author_name": meta["name"],
        "concept_slug": concept_slug,
        "title": post.metadata.get("title", concept_slug),
        "content": post.content,
        "mode": "edit",
    })


@app.post("/{author_slug}/edit/{concept_slug}")
async def edit_concept_save(
    author_slug: str, concept_slug: str,
    title: str = Form(...), content: str = Form(...),
):
    post = read_concept(author_slug, concept_slug)
    sources = post.metadata.get("sources", []) if post else []
    write_concept(author_slug, concept_slug, title, content, sources)
    return RedirectResponse(url=f"/{author_slug}/{concept_slug}", status_code=303)


@app.get("/{author_slug}/new", response_class=HTMLResponse)
async def new_concept_form(request: Request, author_slug: str):
    meta = get_author_meta(author_slug)
    if not meta:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("edit_concept.html", {
        "request": request,
        "author_slug": author_slug,
        "author_name": meta["name"],
        "concept_slug": "",
        "title": "",
        "content": "",
        "mode": "create",
    })


@app.post("/{author_slug}/new")
async def new_concept_save(
    author_slug: str,
    title: str = Form(...), content: str = Form(...),
):
    concept_slug = slugify(title)
    write_concept(author_slug, concept_slug, title, content, sources=["manual"])
    return RedirectResponse(url=f"/{author_slug}/{concept_slug}", status_code=303)


@app.post("/{author_slug}/delete/{concept_slug}")
async def delete_concept_route(author_slug: str, concept_slug: str):
    delete_concept(author_slug, concept_slug)
    return RedirectResponse(url=f"/{author_slug}/", status_code=303)


@app.get("/{author_slug}/{concept_slug}", response_class=HTMLResponse)
async def concept_page(request: Request, author_slug: str, concept_slug: str):
    meta = get_author_meta(author_slug)
    if not meta:
        return RedirectResponse(url="/")

    post = read_concept(author_slug, concept_slug)
    if not post:
        return RedirectResponse(url=f"/{author_slug}/")

    # Get all concept titles for wiki-link resolution
    all_concepts = list_concepts(author_slug)
    titles = [c["title"] for c in all_concepts]

    # Render markdown to HTML
    content_html = markdown.markdown(post.content, extensions=["extra", "smarty"])
    content_html = render_wiki_links(content_html, author_slug, titles)

    return templates.TemplateResponse("concept.html", {
        "request": request,
        "author_slug": author_slug,
        "author_name": meta["name"],
        "concept_slug": concept_slug,
        "title": post.metadata.get("title", concept_slug),
        "sources": post.metadata.get("sources", []),
        "last_updated": post.metadata.get("last_updated", ""),
        "tags": post.metadata.get("tags", []),
        "content_html": content_html,
    })
