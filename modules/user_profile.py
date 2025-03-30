import os
import json

USERS_DIR = "users"


def default_profile(user_id="default"):
    return {
        "user_id": user_id,
        "email": "your@email.com",
        "interests": {
            "keywords": [
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
            ],
            "preferred_channels": ["OpenAI", "Fireship", "Sonny Sangha"],
        },
        "notification_settings": {
            "notification_threshold": 0.5,
            "digest_threshold": 0.3,
            "max_per_digest": 5,
            "cooldown_hours": 12,
        },
    }


def load_user_profile(user_id="default"):
    profile_path = os.path.join(USERS_DIR, user_id, "profile.json")
    if not os.path.exists(profile_path):
        print(f"⚠️ No profile found for user '{user_id}', using default.")
        return default_profile(user_id)

    with open(profile_path, "r", encoding="utf-8") as f:
        profile = json.load(f)
        profile["user_id"] = user_id
        return profile


def load_user_profiles():
    profiles = []
    for uid in os.listdir(USERS_DIR):
        user_dir = os.path.join(USERS_DIR, uid)
        profile_path = os.path.join(user_dir, "profile.json")
        if os.path.isdir(user_dir) and os.path.exists(profile_path):
            with open(profile_path, "r", encoding="utf-8") as f:
                profile = json.load(f)
                profile["user_id"] = uid
                profiles.append(profile)
    return profiles


def extract_keywords(profile):
    return profile.get("interests", {}).get("keywords", [])


if __name__ == "__main__":
    profile = load_user_profile()
    print("Keywords:", extract_keywords(profile))
