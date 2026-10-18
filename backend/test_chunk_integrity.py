
from app.text_chunker import chunk_text


def reconstruct_words(chunks):
    """Reconstruct the original words while removing repeated overlap."""
    if not chunks:
        return []

    reconstructed = chunks[0].split()

    for chunk in chunks[1:]:
        current_words = chunk.split()
        overlap_size = 0

        for size in range(
            min(len(reconstructed), len(current_words)), 0, -1
        ):
            if reconstructed[-size:] == current_words[:size]:
                overlap_size = size
                break

        reconstructed.extend(current_words[overlap_size:])

    return reconstructed


def test_chunks_stay_within_character_limit():
    text = (
        "Python is a programming language. "
        "It is used for data analysis and artificial intelligence. "
        "FastAPI helps developers build APIs."
    )

    chunks = chunk_text(text, chunk_size=60, overlap=10)

    assert chunks, "Expected at least one chunk"
    assert all(len(chunk) <= 60 for chunk in chunks)


def test_original_word_sequence_is_preserved():
    text = (
        "Python is a programming language. "
        "It is used for data analysis and artificial intelligence. "
        "FastAPI helps developers build APIs."
    )

    chunks = chunk_text(text, chunk_size=60, overlap=10)

    assert reconstruct_words(chunks) == text.split()
