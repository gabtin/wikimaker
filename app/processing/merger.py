import logging

from app.processing.llm import chat
from app.processing.prompts import page_generation_instructions, merge_instructions
from app.storage.wiki import read_concept, write_concept, concept_exists, slugify

logger = logging.getLogger(__name__)


async def generate_page(concept: dict, author_name: str, author_slug: str,
                        source_label: str, settings: dict):
    """Generate a new wiki page for a concept, or merge into existing."""
    concept_slug = slugify(concept["title"])

    if concept_exists(author_slug, concept_slug):
        await _merge_into_existing(concept, author_name, author_slug, concept_slug, source_label, settings)
    else:
        await _create_new_page(concept, author_name, author_slug, concept_slug, source_label, settings)


async def _create_new_page(concept: dict, author_name: str, author_slug: str,
                           concept_slug: str, source_label: str, settings: dict):
    """Generate a brand new wiki page for a concept."""
    evidence = "\n".join(f'- "{q}"' for q in concept.get("evidence", []))
    gen_instructions = page_generation_instructions(settings, author_name)

    prompt = f"""Write a wiki page about the concept "{concept['title']}" as discussed by {author_name}.

Context:
- Summary: {concept['summary']}
- Key quotes/evidence:
{evidence}

{gen_instructions}

Write the wiki page content now:"""

    messages = [{"role": "user", "content": prompt}]
    content = await chat(messages)

    write_concept(
        author_slug=author_slug,
        concept_slug=concept_slug,
        title=concept["title"],
        content=content.strip(),
        sources=[source_label],
        extra_meta={"tags": concept.get("tags", [])},
    )
    logger.info("Created new concept page: %s/%s", author_slug, concept_slug)


async def _merge_into_existing(concept: dict, author_name: str, author_slug: str,
                               concept_slug: str, source_label: str, settings: dict):
    """Merge new information into an existing concept page."""
    existing = read_concept(author_slug, concept_slug)
    if not existing:
        return await _create_new_page(concept, author_name, author_slug, concept_slug, source_label, settings)

    evidence = "\n".join(f'- "{q}"' for q in concept.get("evidence", []))
    mrg_instructions = merge_instructions(settings, author_name)

    prompt = f"""Here is an existing wiki page about "{concept['title']}" by {author_name}:

---
{existing.content}
---

Here is new information from a new source ({source_label}):
- Summary: {concept['summary']}
- Key quotes/evidence:
{evidence}

{mrg_instructions}

Return the updated wiki page content:"""

    messages = [{"role": "user", "content": prompt}]
    content = await chat(messages)

    existing_sources = existing.metadata.get("sources", [])
    if source_label not in existing_sources:
        existing_sources.append(source_label)

    existing_tags = existing.metadata.get("tags", [])
    new_tags = concept.get("tags", [])
    combined_tags = sorted(set(existing_tags + new_tags))

    write_concept(
        author_slug=author_slug,
        concept_slug=concept_slug,
        title=concept["title"],
        content=content.strip(),
        sources=existing_sources,
        extra_meta={"tags": combined_tags},
    )
    logger.info("Merged into existing concept page: %s/%s", author_slug, concept_slug)
