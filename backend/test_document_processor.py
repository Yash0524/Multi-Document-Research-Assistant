
from pathlib import Path

from app.document_processor import process_pdf


PDF_PATH = Path(__file__).resolve().parent.parent / "data" / "sample.pdf"


def get_sample_chunks():
    return process_pdf(
        file_path=str(PDF_PATH),
        chunk_size=500,
        overlap=50,
    )


def test_process_pdf_returns_chunks():
    chunks = get_sample_chunks()

    assert len(chunks) > 0


def test_processed_chunks_contain_metadata():
    chunks = get_sample_chunks()

    for chunk in chunks:
        assert chunk["filename"] == "sample.pdf"
        assert isinstance(chunk["page_number"], int)
        assert chunk["page_number"] >= 1
        assert isinstance(chunk["chunk_index"], int)
        assert chunk["chunk_index"] >= 0
        assert isinstance(chunk["text"], str)
        assert chunk["text"].strip()


def test_processed_chunks_respect_character_limit():
    chunks = get_sample_chunks()

    assert all(len(chunk["text"]) <= 500 for chunk in chunks)


def test_processed_chunks_contain_expected_content():
    chunks = get_sample_chunks()
    combined_text = " ".join(chunk["text"] for chunk in chunks)

    assert "Aarsh AI Technologies" in combined_text
    assert "Eligibility criteria" in combined_text
