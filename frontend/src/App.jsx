
import { useEffect, useState } from 'react'

const API_URL = 'http://127.0.0.1:8000'

function App() {
  const [backendInfo, setBackendInfo] = useState(null)
  const [error, setError] = useState('')

  const [selectedFiles, setSelectedFiles] = useState([])
  const [uploadedFiles, setUploadedFiles] = useState([])
  const [isUploading, setIsUploading] = useState(false)
  const [uploadError, setUploadError] = useState('')
  const [uploadMessage, setUploadMessage] = useState('')

  const [question, setQuestion] = useState('')
  const [isSearching, setIsSearching] = useState(false)
  const [searchError, setSearchError] = useState('')
  const [answer, setAnswer] = useState('')
  const [sources, setSources] = useState([])

  // Check whether the backend is available.
  useEffect(() => {
    fetch(`${API_URL}/api/info`)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to connect to the backend')
        }
        return response.json()
      })
      .then((data) => {
        setBackendInfo(data)
        setError('')
      })
      .catch(() => {
        setError('Could not connect to the backend. Is it running?')
      })
  }, [])

  // Validate selected files before uploading.
  function handleFileSelection(event) {
    const files = Array.from(event.target.files || [])
    const invalidFiles = files.filter(
      (file) => !file.name.toLowerCase().endsWith('.pdf'),
    )

    if (invalidFiles.length > 0) {
      setUploadError('Please select PDF files only.')
      setSelectedFiles([])
      event.target.value = ''
      return
    }

    setSelectedFiles(files)
    setUploadError('')
    setUploadMessage('')
  }

  // Upload PDFs and process their contents in the backend.
  async function handleUpload(event) {
    event.preventDefault()

    if (selectedFiles.length === 0) {
      setUploadError('Please select at least one PDF file.')
      return
    }

    setIsUploading(true)
    setUploadError('')
    setUploadMessage('')

    const formData = new FormData()

    selectedFiles.forEach((file) => {
      formData.append('files', file)
    })

    try {
      const response = await fetch(`${API_URL}/api/upload`, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'PDF upload failed.')
      }

      const files = data.files || []

      setUploadedFiles((previousFiles) => {
        const updatedFiles = [...previousFiles]

        files.forEach((file) => {
          const existingIndex = updatedFiles.findIndex(
            (item) => item.filename === file.filename,
          )

          if (existingIndex >= 0) {
            updatedFiles[existingIndex] = file
          } else {
            updatedFiles.push(file)
          }
        })

        return updatedFiles
      })

      setUploadMessage(
        `Successfully processed ${files.length} PDF file(s).`,
      )

      setSelectedFiles([])
      setAnswer('')
      setSources([])
      setSearchError('')
      event.target.reset()
    } catch (err) {
      setUploadError(err.message || 'Could not upload the PDF files.')
    } finally {
      setIsUploading(false)
    }
  }

  // Ask the backend to retrieve evidence and generate an AI answer.
  async function handleSearch(event) {
    event.preventDefault()

    const trimmedQuestion = question.trim()

    if (!trimmedQuestion) {
      setSearchError('Please enter a question.')
      setAnswer('')
      setSources([])
      return
    }

    setIsSearching(true)
    setSearchError('')
    setAnswer('')
    setSources([])

    try {
      const response = await fetch(`${API_URL}/api/answer`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: trimmedQuestion }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to generate an answer.')
      }

      setAnswer(data.answer || '')
      setSources(data.sources || [])
    } catch (err) {
      setSearchError(err.message || 'Could not generate an answer.')
    } finally {
      setIsSearching(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-100 px-4 py-10">
      <main className="mx-auto w-full max-w-3xl rounded-2xl bg-white p-6 shadow-lg sm:p-8">
        <p className="mb-2 text-sm font-semibold uppercase tracking-wider text-blue-600">
          AI Research Workspace
        </p>

        <h1 className="mb-4 text-3xl font-bold text-slate-900">
          Multi-Document Research Assistant
        </h1>

        <p className="mb-6 text-slate-600">
          Upload PDFs, ask questions, and discover evidence supported by your
          documents.
        </p>

        {/* Backend connection */}
        <section className="rounded-lg bg-slate-50 p-4">
          <h2 className="mb-2 font-semibold text-slate-800">
            Backend Connection
          </h2>

          {error ? (
            <p className="text-red-600">{error}</p>
          ) : backendInfo ? (
            <>
              <p className="mb-1 font-medium text-green-700">
                Connected: {backendInfo.status}
              </p>
              <p className="text-sm text-slate-600">
                {backendInfo.message}
              </p>
            </>
          ) : (
            <p className="text-slate-500">Connecting to backend...</p>
          )}
        </section>

        {/* PDF upload */}
        <section className="mt-8 rounded-xl border border-slate-200 p-5">
          <h2 className="mb-2 text-xl font-bold text-slate-900">
            Upload PDF documents
          </h2>

          <p className="mb-4 text-sm text-slate-600">
            Select one or more PDF files to extract their text and add their
            passages to the search database.
          </p>

          <form onSubmit={handleUpload} className="space-y-4">
            <label
              htmlFor="pdf-files"
              className="block text-sm font-medium text-slate-700"
            >
              Choose PDF files
            </label>

            <input
              id="pdf-files"
              type="file"
              accept=".pdf,application/pdf"
              multiple
              disabled={isUploading}
              onChange={handleFileSelection}
              className="block w-full rounded-lg border border-slate-300 p-3 text-sm text-slate-700 file:mr-4 file:rounded-md file:border-0 file:bg-blue-50 file:px-3 file:py-2 file:font-semibold file:text-blue-700 hover:file:bg-blue-100 disabled:opacity-60"
            />

            {selectedFiles.length > 0 && (
              <div className="rounded-lg bg-slate-50 p-3">
                <p className="mb-2 text-sm font-semibold text-slate-700">
                  Selected files ({selectedFiles.length})
                </p>

                <ul className="space-y-1 text-sm text-slate-600">
                  {selectedFiles.map((file, index) => (
                    <li key={`${file.name}-${index}`} className="break-all">
                      {file.name}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <button
              type="submit"
              disabled={isUploading || selectedFiles.length === 0}
              className="w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isUploading ? 'Uploading and processing...' : 'Upload PDFs'}
            </button>
          </form>

          {uploadMessage && (
            <p
              role="status"
              className="mt-4 rounded-lg bg-green-50 p-3 text-sm text-green-700"
            >
              {uploadMessage}
            </p>
          )}

          {uploadError && (
            <p
              role="alert"
              className="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-700"
            >
              {uploadError}
            </p>
          )}

          {uploadedFiles.length > 0 && (
            <div className="mt-5 border-t border-slate-200 pt-4">
              <h3 className="mb-3 font-semibold text-slate-800">
                Processed documents
              </h3>

              <ul className="space-y-3">
                {uploadedFiles.map((file, index) => (
                  <li
                    key={`${file.filename}-${index}`}
                    className="rounded-lg bg-slate-50 p-3"
                  >
                    <p className="break-all font-medium text-slate-800">
                      {file.filename}
                    </p>
                    <p className="mt-1 text-sm text-slate-600">
                      {file.page_count} pages · {file.chunk_count} chunks
                    </p>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>

        {/* Ask questions */}
        <section className="mt-8">
          <h2 className="mb-3 text-xl font-bold text-slate-900">
            Ask your documents
          </h2>

          <form onSubmit={handleSearch} className="space-y-4">
            <label
              htmlFor="question"
              className="block text-sm font-medium text-slate-700"
            >
              Enter your question
            </label>

            <textarea
              id="question"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Example: What are the company's key responsibilities?"
              rows={3}
              disabled={isSearching}
              className="w-full rounded-lg border border-slate-300 p-3 text-slate-800 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100 disabled:bg-slate-100"
            />

            <button
              type="submit"
              disabled={isSearching}
              className="w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isSearching ? 'Generating answer...' : 'Ask your documents'}
            </button>
          </form>

          {searchError && (
            <p
              role="alert"
              className="mt-4 rounded-lg bg-amber-50 p-3 text-sm text-amber-800"
            >
              {searchError}
            </p>
          )}
        </section>

        {/* AI-generated answer */}
        {answer && (
          <section className="mt-8 rounded-xl border border-blue-200 bg-blue-50 p-5">
            <h2 className="mb-3 text-xl font-bold text-slate-900">
              AI-Generated Answer
            </h2>

            <p className="whitespace-pre-wrap break-words leading-7 text-slate-800">
              {answer}
            </p>
          </section>
        )}

        {/* Supporting evidence */}
        {sources.length > 0 && (
          <section className="mt-6">
            <h2 className="mb-2 text-xl font-bold text-slate-900">
              Supporting Evidence
            </h2>

            <p className="mb-4 text-sm text-slate-500">
              Review the passages used to generate the answer.
            </p>

            <div className="space-y-4">
              {sources.map((source, index) => (
                <article
                  key={`${source.filename}-${source.page_number}-${index}`}
                  className="rounded-xl border border-slate-200 bg-white p-4"
                >
                  <p className="whitespace-pre-wrap break-words text-sm leading-7 text-slate-700">
                    {source.text}
                  </p>

                  <div className="mt-4 border-t border-slate-100 pt-3">
                    <p className="text-sm font-semibold text-blue-700">
                      Source: {source.filename}, Page {source.page_number}
                    </p>
                  </div>
                </article>
              ))}
            </div>
          </section>
        )}

        <footer className="mt-8 border-t border-slate-100 pt-4 text-center text-xs text-slate-400">
          Multi-Document Research Assistant · Evidence-based document search
        </footer>
      </main>
    </div>
  )
}

export default App
