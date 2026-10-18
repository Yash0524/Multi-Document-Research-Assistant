
from pathlib import Path

from app.pdf_reader import extract_text_from_pdf


PDF_PATH = Path(__file__).resolve().parent.parent / "data" / "sample.pdf"


def test_pdf_reader_extracts_all_pages():
    pages = extract_text_from_pdf(str(PDF_PATH))

    assert len(pages) == 3


def test_pdf_pages_contain_metadata_and_text():
    pages = extract_text_from_pdf(str(PDF_PATH))

    for page in pages:
        assert page["filename"] == "sample.pdf"
        assert isinstance(page["page_number"], int)
        assert page["page_number"] >= 1
        assert isinstance(page["text"], str)
        assert page["text"].strip()


def test_pdf_reader_extracts_expected_content():
    pages = extract_text_from_pdf(str(PDF_PATH))

    combined_text = " ".join(page["text"] for page in pages)

    assert "Aarsh AI Technologies" in combined_text
    assert "Eligibility criteria" in combined_text
