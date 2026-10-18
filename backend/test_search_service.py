
import pytest

from app.search_service import search_documents


def test_search_returns_relevant_stipend_passage():
    results = search_documents(
        "What is the monthly stipend during the probation period?"
    )

    assert results, "Expected a relevant passage from sample.pdf"
    assert any(
        "15,000 per month" in result["text"]
        for result in results
    )


def test_search_results_include_source_metadata():
    results = search_documents(
        "What is the monthly stipend during the probation period?"
    )

    assert results
    for result in results:
        assert result["filename"]
        assert isinstance(result["page_number"], int)
        assert isinstance(result["distance"], float)
        assert result["distance"] <= 1.15


def test_search_rejects_empty_question():
    with pytest.raises(ValueError, match="Question cannot be empty"):
        search_documents("   ")


def test_search_rejects_invalid_top_k():
    with pytest.raises(ValueError, match="top_k must be at least 1"):
        search_documents("What is the stipend?", top_k=0)
