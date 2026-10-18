import tempfile
from pathlib import Path

from app.document_processor import process_pdf
from app.vector_store import store_chunks

from app.search_service import search_documents
from app.answer_service import answer_question

from fastapi import HTTPException
from app.pdf_reader import extract_text_from_pdf

from fastapi.openapi.utils import get_openapi
from typing import Annotated
from fastapi import File, UploadFile
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Multi-Document Research Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/info")
def get_app_info():
    return {
        "name": "Multi-Document Research Assistant",
        "status": "running",
        "message": "Backend is ready to process research documents."
    }



@app.post("/api/search")
def search_api(payload: dict):
    question = payload.get("question", "").strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    results = search_documents(question)

    return {
        "question": question,
        "results": results,
    }



@app.post("/api/answer")
def answer_api(payload: dict):
    question = payload.get("question", "").strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        return answer_question(question)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate an answer. Please try again.",
        ) from exc




@app.post("/api/upload")
async def upload_pdfs(
    files: Annotated[
        list[UploadFile],
        File(description="Select one or more PDF files"),
    ],
):
    uploaded_files = []

    for file in files:
        filename = Path(file.filename or "").name

        if not filename.lower().endswith(".pdf"):
            await file.close()
            raise HTTPException(
                status_code=400,
                detail=f"{filename} is not a PDF file.",
            )

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir) / filename

                content = await file.read()
                temp_path.write_bytes(content)

                # Extract text and split it into chunks.
                chunks = process_pdf(
                    file_path=str(temp_path),
                    chunk_size=500,
                    overlap=50,
                )

                if not chunks:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            f"No extractable text found in {filename}. "
                            "The PDF may be scanned or image-based."
                        ),
                    )

                # Store the chunks and their source metadata.
                # Use the original upload filename for citations.
                for chunk in chunks:
                    chunk["filename"] = filename

                stored_count = store_chunks(chunks)

                # Extract page information for the API response.
                pages = extract_text_from_pdf(str(temp_path))

                uploaded_files.append({
                    "filename": filename,
                    "page_count": len(pages),
                    "chunk_count": stored_count,
                    "pages": pages,
                })

        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Could not process {filename}: {exc}",
            ) from exc
        finally:
            await file.close()

    return {
        "message": "PDFs processed and stored successfully",
        "files": uploaded_files,
    }






def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    body_schema = schema["components"]["schemas"].get(
        "Body_upload_pdfs_api_upload_post", {}
    )

    files_schema = body_schema.get("properties", {}).get("files", {})
    items_schema = files_schema.get("items", {})

    if items_schema.get("contentMediaType") == "application/octet-stream":
        items_schema.pop("contentMediaType", None)
        items_schema["format"] = "binary"

    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi