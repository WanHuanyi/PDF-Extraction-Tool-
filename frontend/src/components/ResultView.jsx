import React from 'react';

const ResultView = ({ result, sessionId, onReset }) => {
    const { files } = result;
    const baseUrl = `http://localhost:8000/download/${sessionId}`;

    const images = files.filter(f => f.match(/\.(png|jpg|jpeg)$/i));
    const markdown = files.find(f => f.endsWith('.md'));

    return (
        <div className="result-view">
            <div className="result-header">
                <h2>Extraction Complete!</h2>
                <button className="reset-btn" onClick={onReset}>Extract Another</button>
            </div>

            <div className="result-grid">
                <div className="result-card text-card">
                    <h3>📝 Extracted Text</h3>
                    <p>Full content converted to Markdown</p>
                    {markdown && (
                        <a href={`${baseUrl}/${markdown}`} className="download-link" download>
                            Download Markdown
                        </a>
                    )}
                </div>

                <div className="result-card images-card">
                    <h3>🖼️ Extracted Images ({images.length})</h3>
                    <div className="image-grid">
                        {images.map((img, idx) => (
                            <div key={idx} className="image-item">
                                <div className="image-preview">
                                    <img src={`${baseUrl}/${img}`} alt={img} />
                                </div>
                                <div className="image-info">
                                    <span>{img}</span>
                                    <a href={`${baseUrl}/${img}`} download>⬇️</a>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ResultView;
