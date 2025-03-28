# scorer.py

import re

RELEVANCE_THRESHOLD = 0.5

KEYWORDS = [
    "ai agent",
    "openai",
    "gpt",
    "claude",
    "llm",
    "next.js",
    "react",
    "clerk",
    "vercel",
    "postgres",
    "stripe",
    "saas",
    "embedding",
    "autogen",
    "langchain",
    "rag",
    "sora",
    "prompt engineering",
    "agentsdk",
    "autonomous agent",
    "tech stack",
    "semantic kernel",
    "inference",
    "fine-tuning",
    "developer tools",
    "supabase",
    "python",
    "javascript",
    "typescript",
]


def score_relevance(text: str, title: str = "", channel: str = "") -> float:
    text = text.lower()
    title = title.lower()
    channel = channel.lower()

    matches = {"summary": [], "title": [], "channel": []}

    for kw in KEYWORDS:
        pattern = r"\b" + re.escape(kw) + r"\b"
        if re.search(pattern, text):
            matches["summary"].append(kw)
        if re.search(pattern, title):
            matches["title"].append(kw)
        if re.search(pattern, channel):
            matches["channel"].append(kw)

    total_hits = (
        len(matches["summary"])
        + 1.5 * len(matches["title"])
        + 1.2 * len(matches["channel"])
    )
    normalized_score = min(total_hits / 10.0, 1.0)  # Cap score at 1.0

    print(f"🔎 Matched keywords:")
    if any(matches.values()):
        for scope, kws in matches.items():
            if kws:
                print(f"   - {scope}: {', '.join(kws)}")
    else:
        print("   None")

    return round(normalized_score, 2)


if __name__ == "__main__":
    test_summary = "This video introduces new capabilities in OpenAI's GPT for building autonomous AI agents using LangChain and embedding techniques with Vercel."
    test_title = "Build an AI SaaS with LangChain and GPT"
    test_channel = "Fireship"
    print("Score:", score_relevance(test_summary, test_title, test_channel))
