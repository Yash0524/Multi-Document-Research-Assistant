
from app.text_chunker import chunk_page


def get_sample_chunks():
    sample_text = (
        "Python is a programming language. "
        "It is used for data analysis and artificial intelligence. "
        "FastAPI helps developers build APIs."
    )

    return chunk_page(
        text=sample_text,
        filename="sample.pdf",
        page_number=1,
        chunk_size=60,
        overlap=10,
    )


def test_chunk_page_returns_chunks():
    chunks = get_sample_chunks()

    assert len(chunks) > 0


def test_chunks_contain_required_metadata():
    chunks = get_sample_chunks()

    for chunk in chunks:
        assert chunk["filename"] == "sample.pdf"
        assert chunk["page_number"] == 1
        assert "chunk_index" in chunk
        assert isinstance(chunk["text"], str)
        assert chunk["text"].strip()


def test_chunk_indices_are_sequential():
    chunks = get_sample_chunks()

    indices = [chunk["chunk_index"] for chunk in chunks]

    assert indices == list(range(len(chunks)))


def test_chunks_respect_character_limit():
    chunks = get_sample_chunks()

    assert all(len(chunk["text"]) <= 60 for chunk in chunks)
