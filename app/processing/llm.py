import logging
import httpx

from app.config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

logger = logging.getLogger(__name__)

_client: httpx.AsyncClient | None = None


def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            base_url=DEEPSEEK_BASE_URL,
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
            timeout=httpx.Timeout(300.0, connect=30.0),
        )
    return _client


async def chat(messages: list[dict], temperature: float = 0.0) -> str:
    """Send a chat completion request to DeepSeek R1 and return the response text."""
    client = _get_client()

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 8192,
    }

    for attempt in range(3):
        try:
            resp = await client.post("/v1/chat/completions", json=payload)
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            logger.info(
                "LLM call: %d prompt tokens, %d completion tokens",
                usage.get("prompt_tokens", 0),
                usage.get("completion_tokens", 0),
            )
            return content
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429 and attempt < 2:
                import asyncio
                logger.warning("Rate limited, retrying in %d seconds...", 2 ** attempt)
                await asyncio.sleep(2 ** attempt)
                continue
            raise
        except httpx.ReadTimeout:
            if attempt < 2:
                import asyncio
                logger.warning("Read timeout, retrying in %d seconds...", 2 ** attempt)
                await asyncio.sleep(2 ** attempt)
                continue
            raise

    raise RuntimeError("LLM call failed after retries")
