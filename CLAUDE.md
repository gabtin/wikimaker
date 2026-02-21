# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env  # add DEEPSEEK_API_KEY

# Run
wikimaker                        # via installed script
python -m app.cli                # direct
uvicorn app.main:app --reload    # dev with hot-reload

# Tests (once test suite exists)
pytest                           # all tests
pytest tests/unit/               # unit only
pytest tests/integration/        # integration only
pytest tests/e2e/                # end-to-end
pytest tests/unit/test_storage.py::test_slugify  # single test
pytest -k "test_slugify"         # by name pattern
pytest --cov=app --cov-report=term-missing  # with coverage
```

## Architecture

The app is a FastAPI server (`app/main.py`) that is essentially stateless — all persistent state lives in `data/{author-slug}/` as Markdown files with YAML frontmatter (concepts) and a `meta.json`. There is no database.

**Request flow for source ingestion** (the core pipeline):
1. `main.py` route `POST /{author_slug}/add` → ingestion layer
2. `ingestion/` → plain text (`scraper.py` for URLs, `youtube.py` for transcripts, `text.py` for raw input)
3. `processing/extractor.py` → chunks text, calls LLM to extract `[{title, summary, evidence, tags}]`
4. `processing/merger.py` → for each concept, either `write_concept` (new) or merges into existing page via LLM
5. `processing/linker.py` → scans all pages, inserts `[[Wiki Links]]` via regex + LLM relation suggestions
6. `storage/wiki.py` → all file I/O; source of truth for data model

**LLM layer** (`processing/llm.py`): singleton `httpx.AsyncClient`, calls DeepSeek R1 at `deepseek-reasoner`. All LLM calls are async. Prompts are assembled in `processing/prompts.py` using per-wiki `settings` dict.

**Wiki settings** (stored in `meta.json`, defaults in `storage/wiki.py::DEFAULT_SETTINGS`) control LLM behavior: `granularity`, `voice_preservation`, `page_depth`, `critical_lens`, `link_density`, `focus_areas`.

**Wiki-link rendering**: stored as `[[Concept Title]]` in Markdown, resolved to `<a>` tags at read time in `main.py::render_wiki_links()`.

---

## Testing Strategy

### TDD Workflow

Write a failing test first, then implement just enough code to pass it. Commit the failing test and the implementation separately, or together when the cycle is short. The cycle is: **Red → Green → Refactor**.

### Unit Tests (`tests/unit/`)

Test individual functions in isolation. Mock all I/O (file system, LLM calls, HTTP). Fast and deterministic.

**What to unit-test:**
- `storage/wiki.py`: `slugify`, `create_author`, `write_concept`/`read_concept`, `list_concepts`, `get_settings`/`save_settings`, tag aggregation
- `processing/extractor.py`: `_chunk_text`, `_parse_json_response` (with various LLM output formats including malformed ones)
- `processing/linker.py`: wiki-link insertion regex logic, `max_inline` count enforcement
- `main.py`: `render_wiki_links` regex substitution

**Example unit test scope:**
```python
def test_slugify_handles_special_chars():
    assert slugify("Hello, World!") == "hello-world"

def test_parse_json_response_strips_code_fences():
    raw = "```json\n[{\"title\": \"X\"}]\n```"
    assert _parse_json_response(raw) == [{"title": "X"}]
```

### Integration Tests (`tests/integration/`)

Test interactions between layers with real file I/O against a temp directory, but mock LLM calls. Verify the full data lifecycle.

**What to integration-test:**
- Full `create_author` → `save_source` → `write_concept` → `list_concepts` → `read_concept` → `delete_concept` flow
- `generate_page` with mocked `chat()`: assert file is created on disk with correct frontmatter
- `link_concepts` with mocked `chat()`: assert `[[Wiki Links]]` are inserted into concept files
- Settings save/load round-trip

**Setup pattern**: use `tmp_path` fixture (pytest); patch `app.config.DATA_DIR` to point to it. Patch `app.processing.llm.chat` with `AsyncMock`.

### End-to-End Tests (`tests/e2e/`)

Test HTTP routes using FastAPI's `TestClient`. Use real file I/O against a temp `data/` dir, mock only external calls (LLM API, URL scraping, YouTube API).

**User actions to cover:**
| Action | Route | Verify |
|---|---|---|
| Create wiki | `POST /create` | Redirect to `/{slug}/`, `meta.json` exists |
| View wiki list | `GET /` | Author appears in home page |
| Add URL source | `POST /{slug}/add` | Concepts created in `concepts/` |
| Add YouTube source | `POST /{slug}/add` | Transcript fetched, concepts created |
| Add raw text | `POST /{slug}/add` | Concepts created |
| View concept | `GET /{slug}/{concept}` | 200, wiki-links rendered as `<a>` |
| Edit concept | `POST /{slug}/edit/{concept}` | File updated on disk |
| Create concept manually | `POST /{slug}/new` | File created with `sources: ["manual"]` |
| Delete concept | `POST /{slug}/delete/{concept}` | File removed |
| Search by text | `GET /{slug}/search?q=foo` | Relevant results returned |
| Filter by tag | `GET /{slug}/search?tag=foo` | Only tagged concepts returned |
| Update settings | `POST /{slug}/settings` | `meta.json` settings updated |
| Re-tag all | `POST /{slug}/retag` | All concepts get updated tags |
| Delete wiki | `POST /{slug}/delete` | Author directory removed |
| Publication URL | `POST /{slug}/add` | Multiple articles discovered and processed |

### Behaviour-Based Tests (BDD)

Describe tests using the **Given / When / Then** structure in docstrings or as `pytest` parametrize labels. No additional BDD framework required.

**Desirable behaviours to encode:**
- **Idempotency**: ingesting the same source twice does not duplicate concepts; the source hash prevents saving identical text again.
- **Graceful LLM failure**: if `chat()` raises or returns unparseable JSON, the pipeline logs a warning and continues rather than crashing.
- **Concept merging**: a concept that already exists gets its content enriched, not overwritten; sources list is appended.
- **Wiki-link scope**: `[[Link]]` replacements respect `max_inline` per concept; self-links are never inserted.
- **Settings inheritance**: missing settings keys always fall back to `DEFAULT_SETTINGS`.
- **404 resilience**: accessing a non-existent `author_slug` or `concept_slug` redirects rather than returning a 500.

```python
def test_duplicate_source_is_not_reprocessed(tmp_data_dir, mock_chat):
    """
    Given: a source has already been ingested for an author
    When:  the same URL is submitted again
    Then:  no new source file is created and concept count is unchanged
    """
```

---

## Git Workflow

### Branch naming

```
feat/<short-description>     # new feature
fix/<short-description>      # bug fix
refactor/<short-description> # refactoring with no behaviour change
test/<short-description>     # adding or fixing tests
chore/<short-description>    # deps, config, tooling
```

### Commit conventions

Use imperative mood. Single-line for small changes; add a body when the *why* isn't obvious.

```
feat: add PDF ingestion via pdfminer
fix: prevent self-links in wiki-link insertion
test: add unit tests for _parse_json_response edge cases
```

### Workflow

```
main            # production-ready; protected
  └── feat/xyz  # branch off main; PR back to main
```

1. Branch off `main`.
2. Write the failing test(s) first.
3. Implement until tests pass.
4. `git push` and open a PR. Squash-merge into `main` after review.
5. Delete the feature branch after merge.

**Never commit directly to `main`.** Never force-push `main`.
