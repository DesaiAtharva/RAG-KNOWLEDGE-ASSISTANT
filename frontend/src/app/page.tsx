"use client";

import { useState, useRef, useEffect } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: string[];
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    setStatus("Uploading document...");
    
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/upload-document", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setStatus(`Success: ${data.message}`);
      setMessages([{ role: "assistant", content: "I've analyzed your document. What would you like to know?" }]);
    } catch (error) {
      setStatus("Error uploading document.");
      console.error(error);
    } finally {
      setIsUploading(false);
    }
  };

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: input }),
      });
      const data = await response.json();
      const aiMessage: Message = { 
        role: "assistant", 
        content: data.answer,
        sources: data.sources 
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      setMessages((prev) => [...prev, { role: "assistant", content: "Sorry, I encountered an error." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="container">
      <header className="header animate-fade-in">
        <h1 className="title">RAG <span>Knowledge Assistant</span></h1>
        <p className="subtitle">Instant insights from your documents, grounded in truth.</p>
      </header>

      <div className="layout">
        {/* Sidebar / Upload Section */}
        <section className="sidebar glass animate-fade-in">
          <div className="upload-section">
            <h2 className="section-title">Upload Document</h2>
            <div className={`dropzone ${file ? 'has-file' : ''}`}>
              <input 
                type="file" 
                accept=".pdf,.txt" 
                onChange={(e) => setFile(e.target.files?.[0] || null)} 
                className="file-input"
              />
              <div className="dropzone-content">
                {file ? (
                  <p className="file-name">{file.name}</p>
                ) : (
                  <p>Drag & drop or click to select PDF/TXT</p>
                )}
              </div>
            </div>
            <button 
              onClick={handleUpload} 
              disabled={!file || isUploading}
              className="btn btn-primary"
            >
              {isUploading ? "Processing..." : "Process Document"}
            </button>
            {status && <p className="status-msg">{status}</p>}
          </div>

          <div className="info-box glass-card">
            <h3>How it works</h3>
            <ul>
              <li>1. Upload a PDF or Text file.</li>
              <li>2. AI chunks and indexes the content.</li>
              <li>3. Ask questions about the document.</li>
              <li>4. Get answers with source verification.</li>
            </ul>
          </div>
        </section>

        {/* Chat Section */}
        <section className="chat-section glass animate-fade-in">
          <div className="chat-messages" ref={scrollRef}>
            {messages.length === 0 && (
              <div className="empty-state">
                <p>No messages yet. Upload a document to get started!</p>
              </div>
            )}
            {messages.map((msg, i) => (
              <div key={i} className={`message-wrapper ${msg.role}`}>
                <div className="message glass-card">
                  <p className="message-content">{msg.content}</p>
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="sources">
                      <p className="sources-title">Sources:</p>
                      {msg.sources.map((src, j) => (
                        <details key={j} className="source-item">
                          <summary>Context Chunk {j + 1}</summary>
                          <p>{src}</p>
                        </details>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && <div className="loading-dots">AI is thinking...</div>}
          </div>

          <form onSubmit={handleAsk} className="chat-input-area">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about your document..."
              className="chat-input"
            />
            <button type="submit" disabled={isLoading} className="btn btn-send">
              Send
            </button>
          </form>
        </section>
      </div>

      <style jsx>{`
        .container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 2rem;
          min-height: 100vh;
          display: flex;
          flex-direction: column;
        }

        .header {
          text-align: center;
          margin-bottom: 3rem;
        }

        .title {
          font-size: 3rem;
          font-weight: 800;
          letter-spacing: -1px;
        }

        .title span {
          background: linear-gradient(90deg, var(--primary), var(--secondary));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .subtitle {
          color: rgba(255, 255, 255, 0.6);
          margin-top: 0.5rem;
        }

        .layout {
          display: grid;
          grid-template-columns: 350px 1fr;
          gap: 2rem;
          flex-grow: 1;
        }

        .sidebar {
          padding: 1.5rem;
          display: flex;
          flex-direction: column;
          gap: 2rem;
        }

        .section-title {
          font-size: 1.2rem;
          margin-bottom: 1rem;
        }

        .dropzone {
          border: 2px dashed var(--border);
          border-radius: 12px;
          padding: 2rem;
          text-align: center;
          position: relative;
          cursor: pointer;
          transition: all 0.3s ease;
          background: rgba(255, 255, 255, 0.01);
        }

        .dropzone:hover {
          border-color: var(--primary);
          background: rgba(155, 77, 255, 0.05);
        }

        .dropzone.has-file {
          border-color: var(--secondary);
          background: rgba(0, 245, 212, 0.05);
        }

        .file-input {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          opacity: 0;
          cursor: pointer;
        }

        .file-name {
          color: var(--secondary);
          font-weight: 600;
        }

        .btn {
          width: 100%;
          padding: 0.8rem;
          border-radius: 10px;
          border: none;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          margin-top: 1rem;
        }

        .btn-primary {
          background: var(--primary);
          color: white;
        }

        .btn-primary:hover:not(:disabled) {
          filter: brightness(1.1);
          transform: translateY(-2px);
        }

        .btn-primary:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .status-msg {
          margin-top: 1rem;
          font-size: 0.9rem;
          color: var(--secondary);
        }

        .info-box {
          padding: 1.2rem;
        }

        .info-box h3 {
          font-size: 1rem;
          margin-bottom: 0.8rem;
          color: var(--primary);
        }

        .info-box ul {
          list-style: none;
          font-size: 0.85rem;
          color: rgba(255, 255, 255, 0.7);
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .chat-section {
          padding: 1.5rem;
          display: flex;
          flex-direction: column;
          height: 600px;
        }

        .chat-messages {
          flex-grow: 1;
          overflow-y: auto;
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
          padding-right: 0.5rem;
          margin-bottom: 1.5rem;
        }

        .message-wrapper.user {
          align-self: flex-end;
          max-width: 80%;
        }

        .message-wrapper.assistant {
          align-self: flex-start;
          max-width: 80%;
        }

        .message {
          padding: 1rem;
        }

        .message-wrapper.user .message {
          background: rgba(155, 77, 255, 0.1);
          border-color: var(--primary);
        }

        .message-content {
          line-height: 1.5;
        }

        .sources {
          margin-top: 1rem;
          padding-top: 0.8rem;
          border-top: 1px solid var(--border);
        }

        .sources-title {
          font-size: 0.75rem;
          font-weight: 700;
          text-transform: uppercase;
          color: rgba(255, 255, 255, 0.4);
          margin-bottom: 0.5rem;
        }

        .source-item {
          font-size: 0.8rem;
          margin-bottom: 0.4rem;
        }

        .source-item summary {
          cursor: pointer;
          color: var(--secondary);
        }

        .source-item p {
          padding: 0.5rem;
          background: rgba(0, 0, 0, 0.2);
          border-radius: 4px;
          margin-top: 0.3rem;
          font-style: italic;
        }

        .chat-input-area {
          display: flex;
          gap: 1rem;
        }

        .chat-input {
          flex-grow: 1;
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid var(--border);
          border-radius: 12px;
          padding: 1rem;
          color: white;
          outline: none;
          transition: border-color 0.3s ease;
        }

        .chat-input:focus {
          border-color: var(--primary);
        }

        .btn-send {
          width: 100px;
          margin-top: 0;
          background: var(--secondary);
          color: black;
        }

        .empty-state {
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          color: rgba(255, 255, 255, 0.3);
          font-style: italic;
        }

        .loading-dots {
          color: var(--secondary);
          font-size: 0.9rem;
          font-style: italic;
        }

        @media (max-width: 900px) {
          .layout {
            grid-template-columns: 1fr;
          }
          .sidebar {
            height: auto;
          }
        }
      `}</style>
    </main>
  );
}
