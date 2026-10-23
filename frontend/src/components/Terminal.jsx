import React, { useState, useRef, useEffect } from 'react'
import { X, Terminal, ChevronDown, ChevronUp } from 'lucide-react'

const Terminal = ({ onClose }) => {
  const [output, setOutput] = useState([
    { type: 'info', text: 'MuhammedAI Local Developer Terminal' },
    { type: 'info', text: 'Type "help" for available commands' },
  ])
  const [input, setInput] = useState('')
  const [history, setHistory] = useState([])
  const [historyIndex, setHistoryIndex] = useState(-1)
  const [collapsed, setCollapsed] = useState(false)
  const [loading, setLoading] = useState(false)
  const terminalRef = useRef(null)

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight
    }
  }, [output])

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      if (input.trim() && !loading) {
        const command = input.trim()
        setHistory([...history, command])
        setHistoryIndex(-1)
        executeCommand(command)
        setInput('')
      }
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      if (history.length > 0 && historyIndex < history.length - 1) {
        const newIndex = historyIndex + 1
        setHistoryIndex(newIndex)
        setInput(history[history.length - 1 - newIndex])
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault()
      if (historyIndex > 0) {
        const newIndex = historyIndex - 1
        setHistoryIndex(newIndex)
        setInput(history[history.length - 1 - newIndex])
      } else {
        setHistoryIndex(-1)
        setInput('')
      }
    }
  }

  const executeCommand = async (command) => {
    setLoading(true)
    setOutput([...output, { type: 'command', text: `$ ${command}` }])

    try {
      const response = await fetch('/api/editor/terminal/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: command })
      })
      const data = await response.json()

      if (data.success) {
        if (data.stdout) {
          setOutput(prev => [...prev, { type: 'output', text: data.stdout }])
        }
        if (data.stderr) {
          setOutput(prev => [...prev, { type: 'error', text: data.stderr }])
        }
      } else {
        setOutput(prev => [...prev, { type: 'error', text: data.error || 'Command failed' }])
      }
    } catch (error) {
      setOutput(prev => [...prev, { type: 'error', text: `Error: ${error.message}` }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={`terminal-panel ${collapsed ? 'collapsed' : ''}`}>
      <div className="terminal-header">
        <div className="terminal-title">
          <Terminal size={14} />
          <span>Terminal</span>
          {loading && <span className="terminal-loading">●</span>}
        </div>
        <div className="terminal-controls">
          <button onClick={() => setCollapsed(!collapsed)} className="terminal-btn">
            {collapsed ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
          </button>
          <button onClick={onClose} className="terminal-btn">
            <X size={14} />
          </button>
        </div>
      </div>
      {!collapsed && (
        <div className="terminal-content" ref={terminalRef}>
          {output.map((line, index) => (
            <div key={index} className={`terminal-line ${line.type}`}>
              {line.text}
            </div>
          ))}
          <div className="terminal-input-line">
            <span className="prompt">$ </span>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              className="terminal-input"
              autoFocus
              disabled={loading}
            />
          </div>
        </div>
      )}
    </div>
  )
}

export default Terminal
