
import re
from pathlib import Path
from PyPDF2 import PdfReader


def clean_extracted_text(text: str) -> str:
    """Fix known spacing artifacts in the sample PDF."""
    replacements = {
        "T echnical": "Technical",
        "T eams": "Teams",
        "T ranslating": "Translating",
        "T echnologies": "Technologies",
        "W eb": "Web",
        "af filiate": "affiliate",
        "ProductFeedback": "Product Feedback",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"[ \t]+", " ", text)

    return "\n".join(
        line.strip() for line in text.splitlines()
    ).strip()

def extract_text_from_pdf(file_path: str) -> list[dict]:
    """Extract text and metadata from each page of a PDF."""

    pdf_path = Path(file_path)
    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = clean_extracted_text(page.extract_text() or "")

        pages.append({
            "filename": pdf_path.name,
            "page_number": page_number,
            "text": text.strip(),
        })

    return pages