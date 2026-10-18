
from app.pdf_reader import extract_text_from_pdf
from app.text_chunker import chunk_page


def process_pdf(
    file_path: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[dict]:
    """Extract PDF text and convert each page into metadata-rich chunks."""

    pages = extract_text_from_pdf(file_path)
    all_chunks = []

    for page in pages:
        page_chunks = chunk_page(
            text=page["text"],
            filename=page["filename"],
            page_number=page["page_number"],
            chunk_size=chunk_size,
            overlap=overlap,
        )

        all_chunks.extend(page_chunks)

    return all_chunks
