import json
import logging

from app.processing.llm import chat
from app.processing.prompts import extraction_instructions
from app.config import MAX_CHUNK_TOKENS

logger = logging.getLogger(__name__)


def _chunk_text(text: str, max_chars: int = MAX_CHUNK_TOKENS * 4, overlap_chars: int = 800) -> list[str]:
    """Split text into overlapping chunks by character count (rough token approximation)."""
    if len(text) <= max_chars:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        # Try to break at a paragraph boundary
        if end < len(text):
            newline_pos = text.rfind("\n\n", start + max_chars // 2, end)
            if newline_pos > start:
                end = newline_pos
        chunks.append(text[start:end])
        start = end - overlap_chars
    return chunks


def _parse_json_response(text: str) -> list[dict]:
    """Extract JSON array from LLM response, handling markdown code blocks."""
    text = text.strip()
    # Strip markdown code fences
    if text.startswith("```"):
        lines = text.split("\n")
        lines = lines[1:]  # remove opening fence
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)

    # Try to find a JSON array in the response
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1:
        text = text[start:end + 1]

    return json.loads(text)


async def extract_concepts(text: str, author_name: str, settings: dict,
                           existing_titles: list[str] | None = None) -> list[dict]:
    """Extract core concepts from source text.

    Returns list of dicts with keys: title, summary, evidence
    """
    chunks = _chunk_text(text)
    all_concepts = []

    instructions = extraction_instructions(settings, author_name, existing_titles)

    for i, chunk in enumerate(chunks):
        prompt = f"""{instructions}

Text to analyze (chunk {i + 1}/{len(chunks)}):

{chunk}"""

        messages = [{"role": "user", "content": prompt}]
        response = await chat(messages)

        try:
            concepts = _parse_json_response(response)
            all_concepts.extend(concepts)
        except (json.JSONDecodeError, ValueError) as e:
            logger.error("Failed to parse concept extraction response: %s", e)
            continue

    # Deduplicate concepts by title similarity
    if len(chunks) > 1:
        all_concepts = await _deduplicate_concepts(all_concepts, author_name)

    return all_concepts


async def _deduplicate_concepts(concepts: list[dict], author_name: str) -> list[dict]:
    """Use LLM to deduplicate and merge concepts extracted from multiple chunks."""
    concepts_json = json.dumps(concepts, indent=2)
    prompt = f"""Here are concepts extracted from multiple chunks of a text by {author_name}. Some may be duplicates or overlapping.

Merge duplicates into single concepts, combining their summaries, evidence, and tags (union all tags). Keep distinct concepts separate.

Return a clean JSON array with the same format (title, summary, evidence, tags).

Concepts to deduplicate:
{concepts_json}"""

    messages = [{"role": "user", "content": prompt}]
    response = await chat(messages)

    try:
        return _parse_json_response(response)
    except (json.JSONDecodeError, ValueError):
        logger.warning("Deduplication failed, returning raw concepts")
        return concepts
