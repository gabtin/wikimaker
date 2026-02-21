"""Builds prompt fragments from wiki settings.

Each function returns a string that gets injected into the relevant LLM prompt.
Settings dict has keys: purpose, granularity, voice_preservation, page_depth,
critical_lens, focus_areas, link_density.
"""


def extraction_instructions(settings: dict, author_name: str, existing_titles: list[str] | None = None) -> str:
    """Build the extraction prompt based on settings."""

    # --- Granularity → concept count + specificity ---
    granularity_map = {
        "broad": (
            "3-7 high-level themes or major ideas",
            "Focus on the biggest, most important ideas. Combine related sub-ideas into single broad concepts."
        ),
        "standard": (
            "5-15 core concepts, ideas, or frameworks",
            "Balance breadth and specificity. Each concept should be distinct and substantive."
        ),
        "fine": (
            "10-25 specific ideas, arguments, frameworks, and distinctions",
            "Be granular. If the author makes a subtle distinction between two related ideas, treat them as separate concepts. Capture specific frameworks, named ideas, and precise arguments."
        ),
    }
    count_desc, granularity_guidance = granularity_map.get(settings["granularity"], granularity_map["standard"])

    # --- Purpose → what to extract ---
    purpose_map = {
        "personal_reference": "Focus on concepts you'd want to look up later — key frameworks, memorable arguments, actionable ideas, and the author's distinctive terminology.",
        "study_guide": "Focus on concepts that build understanding — core definitions, foundational principles, how ideas connect, and key examples that illustrate each concept.",
        "research_map": "Focus on the author's intellectual contributions — original frameworks, novel arguments, positions in ongoing debates, and how their ideas relate to the broader field.",
        "explain_to_others": "Focus on concepts that someone unfamiliar with this author would need to understand their worldview — the most important and distinctive ideas, explained clearly.",
    }
    purpose_guidance = purpose_map.get(settings["purpose"], purpose_map["personal_reference"])

    # --- Focus areas ---
    focus_str = ""
    if settings.get("focus_areas", "").strip():
        areas = settings["focus_areas"].strip()
        focus_str = f"\nPrioritize concepts related to: {areas}. Still include other important concepts, but weight these areas more heavily."

    # --- Existing concepts awareness ---
    existing_str = ""
    if existing_titles:
        titles_list = ", ".join(f'"{t}"' for t in existing_titles[:30])
        existing_str = f"""
The wiki already has these concept pages: {titles_list}.
When you find information relevant to an existing concept, use that EXACT title so it gets merged into the existing page. Also identify genuinely new concepts not yet covered."""

    # --- Critical lens (affects what evidence to pull) ---
    lens_map = {
        "descriptive": "For evidence, extract quotes that best represent what the author is saying.",
        "analytical": "For evidence, extract quotes that reveal the author's key assumptions, reasoning, and implications — not just conclusions.",
        "critical": "For evidence, extract quotes that show the author's strongest arguments AND any tensions, contradictions, unsupported claims, or notable omissions.",
    }
    lens_guidance = lens_map.get(settings["critical_lens"], lens_map["descriptive"])

    return f"""You are analyzing a text by {author_name}. Extract the {count_desc} from this text.

{granularity_guidance}

{purpose_guidance}
{focus_str}
{existing_str}

For each concept, provide:
- "title": A concise, descriptive title (2-5 words). Use the author's own terminology when they have a specific name for an idea.
- "summary": A 2-3 sentence summary of the concept as presented in this text.
- "evidence": 1-2 relevant direct quotes from the text.
- "tags": 2-5 short lowercase tags categorizing this concept (e.g. "epistemology", "ethics", "decision-making"). Use broad, reusable labels — not the concept title restated.

{lens_guidance}

Return ONLY a JSON array. Example:
[
  {{
    "title": "Creative Destruction",
    "summary": "The author argues that...",
    "evidence": ["quote 1", "quote 2"],
    "tags": ["economics", "innovation"]
  }}
]"""


def page_generation_instructions(settings: dict, author_name: str) -> str:
    """Build instructions for generating a new concept page."""

    # --- Voice preservation ---
    voice_map = {
        "low": "Write in a neutral, encyclopedic third-person tone. Paraphrase the author's ideas into standard academic language.",
        "medium": "Write in a clear, informative tone. Use the author's key terminology and phrases, but explain them. Mix paraphrase with direct quotes.",
        "high": "Preserve the author's voice, terminology, and rhetorical style as much as possible. Use their exact phrases and framing. The page should feel like a distillation of the author's own words, not a third-party summary.",
    }
    voice_guidance = voice_map.get(settings["voice_preservation"], voice_map["medium"])

    # --- Page depth ---
    depth_map = {
        "brief": "Keep it concise: 150-300 words. One overview paragraph, one section with key points, done.",
        "standard": "Aim for 300-600 words. Start with a definition/overview paragraph, then 2-3 sections covering key aspects.",
        "comprehensive": "Write a thorough page: 600-1200 words. Start with an overview, then cover multiple aspects: definition, key arguments, examples, implications, and nuances.",
    }
    depth_guidance = depth_map.get(settings["page_depth"], depth_map["standard"])

    # --- Critical lens ---
    lens_map = {
        "descriptive": "Present the author's ideas faithfully. Your job is to represent their thinking clearly, not to evaluate it.",
        "analytical": "Present the author's ideas, then analyze: what assumptions underlie this concept? What are its implications? How does it connect to the author's broader thinking?",
        "critical": "Present the author's ideas, then engage critically: what are the strengths of this argument? What are its weaknesses or blind spots? Where does it diverge from conventional thinking, and is that divergence justified?",
    }
    lens_guidance = lens_map.get(settings["critical_lens"], lens_map["descriptive"])

    # --- Purpose ---
    purpose_map = {
        "personal_reference": "Write as a useful reference page — someone should be able to quickly look this up and remember the key idea.",
        "study_guide": "Write as a study resource — build understanding step by step, define terms, and use examples to illustrate abstract points.",
        "research_map": "Write as a research reference — situate the idea in context, note its originality, and connect it to related intellectual traditions.",
        "explain_to_others": "Write so that someone completely unfamiliar with this author could understand the concept. Avoid jargon without explanation.",
    }
    purpose_guidance = purpose_map.get(settings["purpose"], purpose_map["personal_reference"])

    return f"""{voice_guidance}

{depth_guidance}

{lens_guidance}

{purpose_guidance}

Use markdown: ## headers to organize sections, > blockquotes for direct quotes from {author_name}.
When referencing other concepts from the wiki, link them inline using [[Concept Title]] syntax naturally within the prose — do NOT create a separate "Related Concepts" section.
Do NOT include a title header (# Title) — the system adds that.
Do NOT include YAML frontmatter."""


def merge_instructions(settings: dict, author_name: str) -> str:
    """Build instructions for merging new info into an existing page."""

    lens_map = {
        "descriptive": "Integrate the new information naturally. If both sources say similar things, strengthen the existing text. If the new source adds new angles, add them.",
        "analytical": "Integrate the new information and deepen the analysis. Note where the new source reinforces, extends, or complicates the existing understanding.",
        "critical": "Integrate the new information critically. Explicitly note where sources agree, where they diverge, and where the new source reveals tensions or contradictions in the author's thinking.",
    }
    lens_guidance = lens_map.get(settings["critical_lens"], lens_map["descriptive"])

    voice_map = {
        "low": "Maintain the neutral, encyclopedic tone.",
        "medium": "Maintain the existing tone. Incorporate new terminology from the author where relevant.",
        "high": "Preserve the author's voice throughout. Weave in new quotes and phrasing from the new source naturally.",
    }
    voice_guidance = voice_map.get(settings["voice_preservation"], voice_map["medium"])

    return f"""Update the page to incorporate the new information.

{lens_guidance}

{voice_guidance}

- Preserve the existing structure but expand where needed.
- Do NOT simply append — weave new information into the existing structure.
- Do NOT include a title header (# Title) or YAML frontmatter.
- Keep using markdown ## headers and > blockquotes for {author_name}'s quotes.
- Keep [[wiki-links]] inline within the prose. Do NOT create a separate "Related Concepts" section."""


def linking_instructions(settings: dict) -> str:
    """Build instructions for how aggressively to suggest cross-links."""
    density_map = {
        "minimal": "Only return pairs with a very strong, direct conceptual relationship. Prefer fewer, higher-quality connections. Return 3-8 pairs maximum.",
        "moderate": "Return pairs that have a meaningful conceptual relationship — they share ideas, one builds on another, or they represent different facets of a theme. Return 5-15 pairs.",
        "dense": "Be generous with connections. Include pairs that are directly related, thematically adjacent, or where understanding one would enrich understanding of the other. Return 10-25 pairs.",
    }
    return density_map.get(settings["link_density"], density_map["moderate"])


def tagging_instructions(title: str, content: str) -> str:
    """Build prompt for retagging an existing concept page."""
    snippet = content[:1500]
    return f"""Assign 2-5 short lowercase tags to this wiki concept. Tags should be broad, reusable categories — not the title restated.

Title: {title}
Content (first 1500 chars): {snippet}

Return ONLY a JSON array of strings. Example: ["economics", "innovation"]"""
