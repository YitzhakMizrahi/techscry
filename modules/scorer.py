# scorer.py

from typing import List

# Basic keyword set (can expand later or make configurable)
KEYWORDS: List[str] = [
    "openai",
    "gpt",
    "llm",
    "sora",
    "chatgpt",
    "ai",
    "agents",
    "multimodal",
    "image generation",
    "voice",
    "autonomous",
    "sam altman",
]

RELEVANCE_THRESHOLD = 0.3  # Can be imported or referenced externally


def score_summary(summary: str) -> float:
    """
    Returns a relevance score between 0.0 and 1.0
    based on keyword matches in the summary text.
    """
    summary_lower = summary.lower()
    match_count = sum(1 for kw in KEYWORDS if kw in summary_lower)
    if not KEYWORDS:
        return 0.0

    score = match_count / len(KEYWORDS)
    return round(score, 2)


if __name__ == "__main__":
    test_summary = "OpenAI released a new voice model that integrates with GPT."
    print(f"Score: {score_summary(test_summary)}")
