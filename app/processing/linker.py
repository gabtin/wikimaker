import json
import logging
import re

from app.processing.llm import chat
from app.processing.prompts import linking_instructions
from app.storage.wiki import list_concepts, read_concept, write_concept

logger = logging.getLogger(__name__)


async def link_concepts(author_slug: str, author_name: str, settings: dict):
    """Scan all concept pages and insert [[wiki-links]] between related concepts."""
    concepts = list_concepts(author_slug)
    if len(concepts) < 2:
        return

    titles = [c["title"] for c in concepts]
    slugs = {c["title"]: c["slug"] for c in concepts}

    # Ask LLM to suggest related concept pairs
    related_pairs = await _suggest_relations(titles, author_name, settings)

    # Determine max inline links from link_density
    max_inline = {"minimal": 1, "moderate": 3, "dense": 5}.get(settings["link_density"], 3)

    for concept_info in concepts:
        slug = concept_info["slug"]
        post = read_concept(author_slug, slug)
        if not post:
            continue

        content = post.content
        title = concept_info["title"]

        # Insert [[wiki-links]] for keyword matches
        for other_title in titles:
            if other_title == title:
                continue
            # Replace plain mentions with wiki-links (case-insensitive, whole word)
            # But don't replace if already inside a wiki-link
            pattern = re.compile(
                r"(?<!\[\[)" + re.escape(other_title) + r"(?!\]\])",
                re.IGNORECASE,
            )
            content = pattern.sub(f"[[{other_title}]]", content, count=max_inline)

        # Remove old Related Concepts section if present (legacy cleanup)
        content = re.sub(
            r"\n## Related Concepts\n.*",
            "",
            content,
            flags=re.DOTALL,
        )

        write_concept(
            author_slug=author_slug,
            concept_slug=slug,
            title=title,
            content=content,
            sources=post.metadata.get("sources", []),
        )

    logger.info("Cross-linking complete for %s (%d concepts)", author_slug, len(concepts))


async def _suggest_relations(titles: list[str], author_name: str, settings: dict) -> list[tuple[str, str]]:
    """Ask LLM to suggest which concepts are related."""
    titles_str = "\n".join(f"- {t}" for t in titles)
    link_guidance = linking_instructions(settings)

    prompt = f"""Here are concept page titles from a wiki about {author_name}'s ideas:

{titles_str}

Which concepts are closely related to each other? Return pairs of related concepts as a JSON array of arrays.

{link_guidance}

Example format:
[["Concept A", "Concept B"], ["Concept C", "Concept D"]]"""

    messages = [{"role": "user", "content": prompt}]
    response = await chat(messages)

    try:
        text = response.strip()
        if text.startswith("```"):
            lines = text.split("\n")[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)
        start = text.find("[")
        end = text.rfind("]")
        if start != -1 and end != -1:
            text = text[start:end + 1]
        pairs = json.loads(text)
        return [(p[0], p[1]) for p in pairs if len(p) == 2]
    except (json.JSONDecodeError, ValueError, IndexError):
        logger.warning("Failed to parse relation suggestions")
        return []
