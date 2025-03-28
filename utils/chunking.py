# chunking.py


def chunk_text(text, max_tokens=2000):
    """
    Splits a long string into chunks of approximately max_tokens words.
    Assumes 1 token ≈ 0.75 words, so we use words as an approximation.
    """
    words = text.split()
    approx_words = int(max_tokens * 1.33)

    chunks = []
    for i in range(0, len(words), approx_words):
        chunk = " ".join(words[i : i + approx_words])
        chunks.append(chunk)

    return chunks


if __name__ == "__main__":
    sample_text = "word " * 10000
    chunks = chunk_text(sample_text)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1} ({len(chunk.split())} words)")
