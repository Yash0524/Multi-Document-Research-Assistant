# Multi-Document Research Assistant

A full-stack Retrieval-Augmented Generation (RAG) application that lets users upload multiple PDF documents, ask questions in natural language, and receive evidence-grounded answers with document and page citations.

## Features

- Upload and process multiple PDF files.
- Extract PDF text and split it into searchable chunks.
- Generate text embeddings using Sentence Transformers.
- Store and retrieve document chunks using ChromaDB.
- Retrieve semantically relevant passages for user questions.
- Generate answers grounded in retrieved evidence using the Google Gemini API.
- Display supporting passages with source filenames and page numbers.
- Abstain when uploaded documents do not contain relevant evidence.

## Technology Stack

- **Frontend:** React, Vite, Tailwind CSS
- **Backend:** Python, FastAPI
- **PDF Processing:** PyPDF2
- **Embeddings:** Sentence Transformers
- **Vector Database:** ChromaDB
- **Answer Generation:** Google Gemini API
- **Testing:** pytest

## Architecture

```text
User
 |
 v
React + Vite Frontend
 |  Upload PDFs / Ask Questions
 v
FastAPI Backend
 |
 |-- PDF text extraction
 |-- Text chunking and metadata
 |-- Sentence Transformer embeddings
 |-- ChromaDB similarity search
 |-- Relevance filtering
 |-- Gemini answer generation using retrieved evidence
 |
 v
Answer + Source Filename + Page Number + Supporting Passages
```

## Prerequisites

- Python 3.13
- Node.js and npm
- A Google Gemini API key for answer generation
- Git (optional, for cloning the repository)

## Setup

The following instructions assume you are using Windows PowerShell from the repository root.

### 1. Set up the backend

Create and activate a Python virtual environment:

```powershell
py -3.13 -m venv backend\.venv
.\backend\.venv\Scripts\Activate.ps1
```

Upgrade pip and install the backend dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn PyPDF2 python-multipart chromadb==1.5.9 sentence-transformers==6.1.0 google-genai==2.31.0 python-dotenv==1.2.4 pytest httpx
```

If a maintained `backend/requirements.txt` file is available, use that file as the preferred dependency installation method instead:

```powershell
python -m pip install -r backend\requirements.txt
```

Create a file named `.env` inside the `backend` directory:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash
```

Replace the placeholder with your own Gemini API key.

**Security:** Never commit `backend/.env`, expose API keys in frontend code, or publish secrets in logs or screenshots.

### 2. Start the backend

From the repository root, with the virtual environment activated, run:

```powershell
cd backend
python -m uvicorn app.main:app --reload
```

The backend runs at:

- **API:** http://127.0.0.1:8000
- **Interactive API documentation:** http://127.0.0.1:8000/docs
- **Health check:** http://127.0.0.1:8000/health

Keep this terminal open while using the application.

### 3. Set up and start the frontend

Open a second PowerShell terminal and navigate to the frontend directory:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite, typically:

http://localhost:5173

Keep both the frontend and backend running while testing the application.

## How to Use

1. Start the backend and frontend.
2. Open the frontend in your browser.
3. Upload one or more PDF documents.
4. Ask a question whose answer is expected to appear in the uploaded documents.
5. Review the generated answer and its supporting evidence.
6. Check the cited filename and page number against the original PDF.
7. Ask a question unrelated to the uploaded documents to test whether the application abstains when relevant evidence is unavailable.

## API Overview

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Check backend health |
| `GET` | `/api/info` | Retrieve application information |
| `POST` | `/api/upload` | Upload and process PDF files |
| `POST` | `/api/search` | Retrieve relevant document passages |
| `POST` | `/api/answer` | Generate an evidence-grounded answer |

Open http://127.0.0.1:8000/docs to inspect the available endpoints and their request and response schemas.

## Tests and Quality Checks

### Backend automated tests

The backend currently has **17 passing automated tests** covering PDF extraction, text chunking, chunk integrity, document processing, and semantic search.

From the repository root, activate the environment if necessary and run:

```powershell
cd backend
python -m pytest -v
```

To check whether installed Python dependencies are consistent, run:

```powershell
python -m pip check
```

### Frontend checks

Open a separate terminal, navigate to the frontend directory, and run:

```powershell
cd frontend
npm run lint
npm run build
```

These commands check code quality and verify that the frontend can be built for production.

### Manual end-to-end testing

Automated tests do not replace testing the full application. Use the checklist below to verify application behavior through the running frontend and backend.

## Manual End-to-End Test Checklist

- [ ] Upload a valid PDF and confirm the application reports success.
- [ ] Ask a question with a known answer and verify the cited filename and page number.
- [ ] Inspect the supporting passages and confirm they are relevant to the question.
- [ ] Ask a question whose answer is absent from all uploaded PDFs and verify that the application abstains without unsupported citations.
- [ ] Try an invalid or non-PDF upload and verify that the application handles the error gracefully.
- [ ] Upload the same PDF twice and verify that duplicate chunks do not accumulate unexpectedly.
- [ ] Restart the backend and verify that persisted ChromaDB data behaves as intended.

## Current Limitations and Future Improvements

- **Retrieval quality:** The current distance threshold is provisional. Its effectiveness should be evaluated against a larger set of questions and documents.
- **Document identification:** Stable document IDs or content hashes could distinguish files with identical filenames and help prevent stale or duplicate chunks.
- **PDF validation:** Add file-size and page-count limits, along with clearer error handling for malformed or encrypted PDFs.
- **Scanned PDFs:** Add OCR support for documents that contain images instead of extractable text.
- **Testing:** Expand automated coverage for answer grounding, duplicate uploads, API error handling, and additional retrieval scenarios.
- **Deployment:** Configure CORS and the frontend API URL for the deployment environment.
- **Security and reliability:** Consider authentication, rate limiting, upload restrictions, and secure secret management before public deployment.

## Security and Privacy

- Keep `backend/.env` and local vector database files out of version control.
- Never expose the Gemini API key in frontend code or public logs.
- Only upload documents you are authorized to process.
- Be mindful that uploaded PDFs may contain confidential or personally identifiable information.
- Review generated answers and cited evidence rather than assuming every generated answer is correct.

## Project Status

**Working MVP:** PDF upload, semantic retrieval, Gemini-based answers, source citations, and abstention have been manually verified.

The backend currently has **17 passing automated tests** covering PDF extraction, chunking, document processing, and retrieval. Frontend linting, the production build, and Python dependency checks have also passed.

Retrieval quality across diverse documents, duplicate-upload handling, and broader API failure scenarios remain areas for improvement.
