import React, { useState, useRef } from 'react';

const UploadZone = ({ onFileSelect, isUploading }) => {
    const [dragActive, setDragActive] = useState(false);
    const inputRef = useRef(null);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            onFileSelect(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            onFileSelect(e.target.files[0]);
        }
    };

    const onButtonClick = () => {
        inputRef.current.click();
    };

    return (
        <div
            className={`upload-zone ${dragActive ? "drag-active" : ""}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
        >
            <input
                ref={inputRef}
                type="file"
                className="upload-input"
                onChange={handleChange}
                accept=".pdf"
            />
            <div className="upload-content">
                <div className="upload-icon">📄</div>
                <h3>Upload your PDF</h3>
                <p>Drag & drop or click to browse</p>
                <button className="upload-btn" onClick={onButtonClick} disabled={isUploading}>
                    {isUploading ? "Processing..." : "Select File"}
                </button>
            </div>
        </div>
    );
};

export default UploadZone;
