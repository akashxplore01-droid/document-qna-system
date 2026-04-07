import React, { useState, useRef, useEffect } from 'react';
import './ChatArea.css';
import { FiSend, FiLoader } from 'react-icons/fi';
import ReactMarkdown from 'react-markdown';

function ChatArea({ chatHistory, onAsk, loading }) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  const handleSend = () => {
    if (input.trim() && !loading) {
      onAsk(input);
      setInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !loading) {
      handleSend();
    }
  };

  return (
    <div className="main-content">
      <div className="chat-header">
        <h2>📄 DocQA - Document Question Answering</h2>
      </div>

      <div className="chat-container">
        {chatHistory.length === 0 ? (
          <div className="welcome">
            <h2>Welcome to DocQA</h2>
            <p>Upload a PDF document and start asking questions</p>
          </div>
        ) : (
          <div className="messages">
            {chatHistory.map((msg) => (
              <div key={msg.id}>
                <div className="message user-message">
                  <div className="user-content">
                    {msg.query}
                  </div>
                </div>
                <div className="message">
                  <div className="assistant-content">
                    <ReactMarkdown>{msg.answer}</ReactMarkdown>
                    <div className="tool-indicator">
                      Tool: <strong>{msg.tool}</strong>
                    </div>
                  </div>
                </div>
              </div>
            ))}
            {loading && (
              <div className="message">
                <div className="assistant-content loading">
                  <FiLoader className="spinner" /> Thinking...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <div className="input-area">
        <input
          type="text"
          placeholder="Ask a question about the document..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading}>
          {loading ? <FiLoader className="spinner" /> : <FiSend />}
        </button>
      </div>
    </div>
  );
}

export default ChatArea;