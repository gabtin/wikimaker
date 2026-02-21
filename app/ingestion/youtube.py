import re

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"(?:embed/)([a-zA-Z0-9_-]{11})",
        r"(?:shorts/)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from URL: {url}")


def fetch_youtube_transcript(url: str) -> str:
    """Fetch transcript text from a YouTube video URL."""
    video_id = extract_video_id(url)
    ytt_api = YouTubeTranscriptApi()
    try:
        transcript = ytt_api.fetch(video_id)
    except Exception as e:
        raise ValueError(f"Could not fetch transcript: {e}")

    text = " ".join(snippet.text for snippet in transcript)
    # Clean up common transcript artifacts
    text = re.sub(r"\s+", " ", text).strip()
    return text
