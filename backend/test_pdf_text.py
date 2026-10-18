
from app.pdf_reader import extract_text_from_pdf

pages = extract_text_from_pdf("../data/sample.pdf")

for page in pages:
    print(f"\n--- PAGE {page['page_number']} ---")
    print(page["text"])
