# smart_scorer.py
import os
from openai import OpenAI
from modules.user_profile import load_user_profile

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL_SMART_SCORER = os.getenv("MODEL_SMART_SCORER", "gpt-3.5-turbo")

models = client.models.list()

print("✅ Models loaded:", [m.id for m in models.data[:3]])


def smart_score(summary: str, user_id: str) -> float:
    profile = load_user_profile(user_id)
    return smart_score_summary(summary, profile)


def smart_score_summary(summary: str, profile: dict, verbose=False) -> float:
    keywords = profile.get("interests", {}).get("keywords", [])
    channels = profile.get("interests", {}).get("preferred_channels", [])

    interest_description = (
        f"The user is interested in topics such as: {', '.join(keywords)}.\n"
    )
    interest_description += f"They follow YouTube channels: {', '.join(channels)}."

    prompt = (
        "You are a relevance scorer AI. Based on the user profile and the summary below, "
        "assign a relevance score from 0.0 (not relevant) to 1.0 (highly relevant).\n"
        f"User Profile:\n{interest_description}\n"
        f"Summary:\n{summary}\n"
        "Respond only with the score as a decimal number."
    )

    if verbose:
        print("🧠 [Smart Scorer Prompt] ------------------")
        print(prompt)
        print("------------------------------------------")

    try:
        response = client.chat.completions.create(
            model=MODEL_SMART_SCORER,
            messages=[{"role": "user", "content": prompt}],
        )
        score_str = response.choices[0].message.content.strip()
        return max(0.0, min(1.0, float(score_str)))
    except Exception as e:
        print(f"⚠️ Error in smart scorer: {e}")
        return 0.0


if __name__ == "__main__":
    test_summary = "This video explains how to use OpenAI GPT-4, Next.js 15, and Clerk for building a full-stack AI SaaS."
    score = smart_score(test_summary, user_id="user123")
    print("Smart Relevance Score:", score)
