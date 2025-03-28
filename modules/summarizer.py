import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
USE_MOCK = False

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_text(text):
    if USE_MOCK:
        return f"[Mock Summary] {text[:150]}..."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the following tech video transcript.",
                },
                {"role": "user", "content": text},
            ],
            temperature=0.5,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ Error during summarization: {e}")
        return None


if __name__ == "__main__":
    long_text = """
    In this video, we dive into the latest updates from OpenAI and explore how GPT-4 is evolving...
    """
    summary = summarize_text(long_text)
    print("\nSummary:\n", summary)
