# WikiMaker Project Context

WikiMaker is an automated knowledge management system that synthesizes structured wikis from diverse sources (URLs, YouTube videos, and text). It leverages the DeepSeek R1 language model to perform high-fidelity concept extraction, page generation, and semantic cross-linking.

## Project Overview

- **Purpose:** To create searchable, interconnected, and thematic wikis from a body of work (e.g., an author's articles, a set of lectures, or research papers).
- **Core Workflow:** 
    1. **Ingest:** Scrape URLs, fetch YouTube transcripts, or accept raw text.
    2. **Extract:** Use DeepSeek R1 to identify key concepts based on configurable granularity.
    3. **Generate:** Create descriptive Markdown pages for each concept, preserving the author's voice or applying a critical lens.
    4. **Link:** Automatically identify and insert `[[Wiki Links]]` between related concepts.
    5. **Manage:** Search, tag, edit, and update concepts as new information is added.

## Technical Stack

- **Backend:** FastAPI (Python 3.11+)
- **LLM Provider:** DeepSeek R1 (`deepseek-reasoner`) via HTTP API.
- **Data Ingestion:** `trafilatura` (Web scraping), `youtube-transcript-api`.
- **Storage:** Local file system using Markdown files with YAML frontmatter for concept pages and JSON for metadata.
- **Frontend:** Jinja2 templates, Vanilla CSS, and minimal JavaScript for UI interactions.
- **Key Libraries:** `python-frontmatter`, `markdown`, `httpx`, `uvicorn`.

## Directory Structure

- `app/`: Core application logic.
    - `ingestion/`: Modules for scraping and fetching external content.
    - `processing/`: LLM orchestration—extraction, merging, linking, and prompt management.
    - `storage/`: File-based persistence layer and data model management.
    - `templates/` & `static/`: Web UI components.
    - `cli.py` & `main.py`: Application entry points.
- `data/`: The storage root for generated wikis.
    - `{author-slug}/`:
        - `meta.json`: Wiki-level metadata and settings.
        - `_sources/`: Raw text of ingested sources.
        - `concepts/`: Generated Markdown concept pages.
- `.env`: Environment configuration (requires `DEEPSEEK_API_KEY`).

## Building and Running

### Prerequisites
- Python 3.11+
- DeepSeek API Key

### Setup
1. Create a virtual environment: `python -m venv .venv`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment: `cp .env.example .env` and add your `DEEPSEEK_API_KEY`.

### Running the Application
- **Web Interface:** Run `python -m app.cli` or use the installed script: `wikimaker`.
- **Default URL:** `http://127.0.0.1:8000`

## Development Conventions

- **LLM Settings:** Wiki behavior is governed by settings in `app/storage/wiki.py` (e.g., `granularity`, `voice_preservation`, `critical_lens`). Prompts are dynamically built in `app/processing/prompts.py`.
- **Wiki Linking:** Concepts are linked using `[[Concept Title]]` syntax. The system automatically resolves these to slugs and generates `<a>` tags during HTML rendering.
- **State Management:** The application is largely stateless; all permanent state is derived from the files in the `data/` directory.
- **Concurrency:** LLM calls are asynchronous and handled via `httpx.AsyncClient` in `app/processing/llm.py`.

## Future Considerations
- Support for PDF ingestion.
- Vector-based search for larger wikis.
- Multi-author cross-wiki linking.
- Export to static sites (e.g., Hugo, Obsidian).
