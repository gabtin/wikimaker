# wikimaker

A self-hosted, LLM-powered personal wiki builder. Feed it URLs, YouTube videos, or raw text — it extracts concepts, merges related ideas, and weaves them together with `[[Wiki Links]]` automatically.

## How it works

1. **Ingest** a source (URL, YouTube link, or plain text)
2. **Extract** concepts via DeepSeek R1 — each becomes a wiki page with a title, summary, evidence, and tags
3. **Merge** new concepts into existing pages when they overlap, enriching rather than duplicating
4. **Link** pages together automatically with `[[Wiki Links]]`

All data is stored as Markdown files with YAML frontmatter — no database.

## Setup

**Requirements:** Python 3.11+, a [DeepSeek API key](https://platform.deepseek.com/)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env   # add your DEEPSEEK_API_KEY
```

## Run

```bash
wikimaker                        # via installed script
python -m app.cli                # direct
uvicorn app.main:app --reload    # dev with hot-reload
```

Then open `http://localhost:8000`.

## Docker

```bash
docker build -t wikimaker .
docker run -p 8000:8000 -v $(pwd)/data:/app/data wikimaker
```

## Project structure

```
app/
  main.py            # FastAPI routes, wiki-link rendering
  cli.py             # entry point
  config.py          # DATA_DIR and env config
  ingestion/
    scraper.py       # URL → plain text (trafilatura)
    youtube.py       # YouTube → transcript
    text.py          # raw text passthrough
  processing/
    extractor.py     # chunk text → LLM → [{title, summary, evidence, tags}]
    merger.py        # new concept → write or merge into existing page
    linker.py        # insert [[Wiki Links]] across all pages
    llm.py           # async DeepSeek client
    prompts.py       # prompt templates
  storage/
    wiki.py          # all file I/O, data model, DEFAULT_SETTINGS
  templates/         # Jinja2 HTML templates
  static/            # CSS
data/
  {author-slug}/
    meta.json        # wiki settings
    concepts/
      {concept-slug}.md
```

## Wiki settings

Each wiki has configurable LLM behavior stored in `meta.json`:

| Setting | Description |
|---|---|
| `granularity` | How finely to split concepts |
| `voice_preservation` | Preserve the source's writing style |
| `page_depth` | Detail level per concept page |
| `critical_lens` | Analytical perspective applied |
| `link_density` | How many `[[Wiki Links]]` to insert |
| `focus_areas` | Topics to emphasize during extraction |

## Tech stack

- **FastAPI** — HTTP server
- **DeepSeek R1** (`deepseek-reasoner`) — LLM for extraction, merging, linking
- **trafilatura** — web scraping
- **youtube-transcript-api** — YouTube transcripts
- **Jinja2** — HTML templates
- **python-frontmatter** — Markdown + YAML storage
