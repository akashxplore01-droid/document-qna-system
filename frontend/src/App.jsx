import React, { useState, useEffect } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import axios from 'axios';

function App() {
  const [documents, setDocuments] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentDoc, setCurrentDoc] = useState(null);

  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

  const handleUpload = async (file) => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE}/documents/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setDocuments([...documents, response.data]);
      setCurrentDoc(response.data.filename);
      alert('Document uploaded successfully!');
    } catch (error) {
      alert('Error uploading document: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async (query) => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE}/chat/ask`, { query });
      const newMessage = {
        id: Date.now(),
        query,
        answer: response.data.answer,
        tool: response.data.tool,
        timestamp: new Date()
      };
      setChatHistory([...chatHistory, newMessage]);
    } catch (error) {
      alert('Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = async () => {
    try {
      await axios.delete(`${API_BASE}/chat/history`);
      setChatHistory([]);
    } catch (error) {
      alert('Error clearing history: ' + error.message);
    }
  };

  return (
    <div className="app">
      <Sidebar 
        documents={documents}
        onUpload={handleUpload}
        onClearHistory={handleClearHistory}
        loading={loading}
      />
      <ChatArea 
        chatHistory={chatHistory}
        onAsk={handleAsk}
        loading={loading}
      />
    </div>
  );
}

export default App;