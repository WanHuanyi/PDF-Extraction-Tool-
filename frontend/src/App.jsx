import React, { useState } from 'react';
import UploadZone from './components/UploadZone';
import ResultView from './components/ResultView';
import './App.css'; // We'll use App.css or index.css

function App() {
  const [result, setResult] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileSelect = async (file) => {
    setIsUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/extract', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Extraction failed');
      }

      const data = await response.json();
      setResult(data);
      setSessionId(data.session_id);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsUploading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setSessionId(null);
    setError(null);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>PDF Extractor Pro</h1>
        <p>Extract text, tables, and images with ease</p>
      </header>

      <main className="app-main">
        {error && <div className="error-message">{error}</div>}

        {!result ? (
          <UploadZone onFileSelect={handleFileSelect} isUploading={isUploading} />
        ) : (
          <ResultView result={result} sessionId={sessionId} onReset={handleReset} />
        )}
      </main>
    </div>
  );
}

export default App;
