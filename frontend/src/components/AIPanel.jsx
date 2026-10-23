import React, { useState, useRef, useEffect } from 'react'
import { X, Send, Bot, Loader2 } from 'lucide-react'

const AIPanel = ({ onClose }) => {
  const [messages, setMessages] = useState([
    { 
      role: 'assistant', 
      content: 'Hello! I\'m your AI coding assistant. How can I help you today?' 
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesRef = useRef(null)

  useEffect(() => {
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight
    }
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    setInput('')
    setMessages([...messages, { role: 'user', content: userMessage }])
    setLoading(true)

    try {
      // Backend API'ye istek gönder
      const response = await fetch('/api/agent/run', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ task: userMessage }),
      })

      if (response.ok) {
        const data = await response.json()
        setMessages([
          ...messages,
          { role: 'user', content: userMessage },
          { role: 'assistant', content: data.response || 'Task completed successfully' }
        ])
      } else {
        // Mock response if backend fails
        setTimeout(() => {
          setMessages(prev => [
            ...prev,
            { 
              role: 'assistant', 
              content: `I understand you want to: "${userMessage}".\n\nThis is a mock response. The backend integration will provide real AI responses.` 
            }
          ])
          setLoading(false)
        }, 1000)
      }
    } catch (error) {
      // Mock response on error
      setTimeout(() => {
        setMessages(prev => [
          ...prev,
          { 
            role: 'assistant', 
            content: `I understand you want to: "${userMessage}".\n\nThis is a mock response. The backend integration will provide real AI responses.` 
          }
        ])
        setLoading(false)
      }, 1000)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="ai-panel">
      <div className="ai-header">
        <div className="ai-title">
          <Bot size={14} />
          <span>AI Assistant</span>
        </div>
        <button onClick={onClose} className="ai-close-btn">
          <X size={14} />
        </button>
      </div>
      <div className="ai-content" ref={messagesRef}>
        {messages.map((message, index) => (
          <div key={index} className={`ai-message ${message.role}`}>
            <div className="message-role">
              {message.role === 'user' ? 'You' : 'AI'}
            </div>
            <div className="message-content">
              {message.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="ai-message assistant">
            <div className="message-role">AI</div>
            <div className="message-content">
              <div className="loading-spinner"></div>
              Thinking...
            </div>
          </div>
        )}
      </div>
      <div className="ai-input">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask AI to help with your code..."
          disabled={loading}
        />
        <button 
          onClick={handleSend} 
          className="ai-button"
          disabled={loading || !input.trim()}
        >
          {loading ? (
            <Loader2 size={16} className="spin" />
          ) : (
            <Send size={16} />
          )}
          <span>Send</span>
        </button>
      </div>
    </div>
  )
}

export default AIPanel
