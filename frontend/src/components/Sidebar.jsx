import React, { useRef } from 'react';
import './Sidebar.css';
import { FiUpload, FiTrash2 } from 'react-icons/fi';

function Sidebar({ documents, onUpload, onClearHistory, loading }) {
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      onUpload(file);
    } else {
      alert('Please select a valid PDF file');
    }
  };

  const handleDragDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const files = e.dataTransfer.files;
    if (files.length > 0 && files[0].type === 'application/pdf') {
      onUpload(files[0]);
    }
  };

  return (
    <div className="sidebar">
      <h1 className="logo">DocQA</h1>
      
      <div
        className="upload-area"
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDragDrop}
      >
        <FiUpload size={24} />
        <p>Drag PDF here</p>
        <p className="or">or</p>
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={loading}
        >
          Browse
        </button>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileSelect}
          accept=".pdf"
          style={{ display: 'none' }}
        />
      </div>

      <div className="documents-section">
        <h3>Documents</h3>
        <div className="documents-list">
          {documents.length === 0 ? (
            <p className="empty">No documents yet</p>
          ) : (
            documents.map((doc, idx) => (
              <div key={idx} className="document-item">
                <span>{doc.filename}</span>
                <small>{doc.chunks} chunks</small>
              </div>
            ))
          )}
        </div>
      </div>

      <button className="clear-btn" onClick={onClearHistory}>
        <FiTrash2 /> Clear History
      </button>

      <div className="footer">
        <p>Developed by:</p>
        <small>Omkar Ganesh Dahibhate</small>
        <small>Akash Arun Sanap</small>
        <small>Aniket Rajesh Gaikwad</small>
      </div>
    </div>
  );
}

export default Sidebar;