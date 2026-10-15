
import { useEffect, useState } from 'react'

function App() {
  const [backendInfo, setBackendInfo] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/info')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to connect to the backend')
        }
        return response.json()
      })
      .then((data) => setBackendInfo(data))
      .catch(() => {
        setError('Could not connect to the backend. Is it running?')
      })
  }, [])

  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center p-6">
      <div className="w-full max-w-lg rounded-2xl bg-white p-8 shadow-lg">
        <p className="mb-2 text-sm font-semibold uppercase tracking-wider text-blue-600">
          AI Research Workspace
        </p>

        <h1 className="mb-4 text-3xl font-bold text-slate-900">
          Multi-Document Research Assistant
        </h1>

        <p className="mb-6 text-slate-600">
          Upload PDFs, ask questions, and discover answers supported by your documents.
        </p>

        <div className="rounded-lg bg-slate-50 p-4">
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
              <p className="text-sm text-slate-600">{backendInfo.message}</p>
            </>
          ) : (
            <p className="text-slate-500">Connecting to backend...</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
