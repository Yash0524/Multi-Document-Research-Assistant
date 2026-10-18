
import re




def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[str]:
    """Split text into overlapping chunks without losing words."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    text = text.strip()
    if not text:
        return []

    words = text.split()

    # Reject words that cannot fit into a chunk.
    if any(len(word) > chunk_size for word in words):
        raise ValueError("A word exceeds chunk_size; increase chunk_size.")

    chunks = []
    start = 0

    while start < len(words):
        end = start
        length = 0

        # Add as many whole words as fit.
        while end < len(words):
            added_length = len(words[end])
            if end > start:
                added_length += 1

            if length + added_length > chunk_size:
                break

            length += added_length
            end += 1

        chunks.append(" ".join(words[start:end]))

        if end >= len(words):
            break

        # Start the next chunk with whole words from the previous chunk.
        next_start = end
        overlap_length = 0

        while next_start > start:
            word = words[next_start - 1]
            added_length = len(word) + (1 if overlap_length else 0)

            if overlap_length + added_length > overlap:
                break

            overlap_length += added_length
            next_start -= 1

        # Always advance, even when no whole word fits in the overlap.
        start = next_start if next_start > start else end

    return chunks






def chunk_page(
    text: str,
    filename: str,
    page_number: int,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[dict]:
    """Split a page and attach its source metadata."""

    text_chunks = chunk_text(
        text,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    return [
        {
            "text": text_chunk,
            "filename": filename,
            "page_number": page_number,
            "chunk_index": index,
        }
        for index, text_chunk in enumerate(text_chunks)
    ]
