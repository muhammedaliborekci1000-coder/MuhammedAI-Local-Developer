import React, { useState, useEffect } from 'react'
import { Terminal, Bot, GitBranch, CheckCircle, AlertCircle, Bug, Users } from 'lucide-react'

const StatusBar = ({ 
  onToggleTerminal, 
  onToggleAI, 
  onToggleDebugger,
  onToggleCollaboration,
  terminalVisible, 
  aiPanelVisible,
  debuggerVisible,
  collaborationVisible,
  activeFile 
}) => {
  const [gitStatus, setGitStatus] = useState({ branch: 'main', changed: 0, staged: 0, untracked: 0 })

  useEffect(() => {
    loadGitStatus()
    // Her 5 saniyede bir git status güncelle
    const interval = setInterval(loadGitStatus, 5000)
    return () => clearInterval(interval)
  }, [])

  const loadGitStatus = async () => {
    try {
      const response = await fetch('/api/editor/git/status')
      const data = await response.json()
      if (data.success) {
        setGitStatus(data)
      }
    } catch (error) {
      console.error('Failed to load git status:', error)
    }
  }

  return (
    <div className="status-bar">
      <div className="status-left">
        <div className="status-item" onClick={onToggleTerminal}>
          <Terminal size={14} />
          <span>Terminal</span>
        </div>
        <div className="status-item" onClick={onToggleAI}>
          <Bot size={14} />
          <span>AI Assistant</span>
        </div>
        <div className="status-item" onClick={onToggleDebugger}>
          <Bug size={14} />
          <span>Debugger</span>
        </div>
        <div className="status-item" onClick={onToggleCollaboration}>
          <Users size={14} />
          <span>Collaboration</span>
        </div>
        <div className="status-item">
          <GitBranch size={14} />
          <span>{gitStatus.branch}</span>
          {gitStatus.changed > 0 && <span className="git-changed">+{gitStatus.changed}</span>}
        </div>
        <div className="status-item">
          {gitStatus.changed === 0 ? (
            <CheckCircle size={14} />
          ) : (
            <AlertCircle size={14} />
          )}
          <span>{gitStatus.changed} Changes</span>
        </div>
      </div>
      <div className="status-right">
        {activeFile && (
          <div className="status-item">
            <span>{activeFile.path}</span>
          </div>
        )}
        <div className="status-item">
          <span>Python 3.11</span>
        </div>
        <div className="status-item">
          <span>UTF-8</span>
        </div>
        <div className="status-item">
          <span>Ln 1, Col 1</span>
        </div>
      </div>
    </div>
  )
}

export default StatusBar
