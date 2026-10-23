import React, { useState, useEffect } from 'react'
import FileTree from './components/FileTree'
import Editor from './components/Editor'
import Terminal from './components/Terminal'
import StatusBar from './components/StatusBar'
import AIPanel from './components/AIPanel'
import Debugger from './components/Debugger'
import Collaboration from './components/Collaboration'
import './App.css'

function App() {
  const [activeFile, setActiveFile] = useState(null)
  const [openTabs, setOpenTabs] = useState([])
  const [activeTab, setActiveTab] = useState(null)
  const [terminalVisible, setTerminalVisible] = useState(true)
  const [aiPanelVisible, setAiPanelVisible] = useState(true)
  const [debuggerVisible, setDebuggerVisible] = useState(false)
  const [collaborationVisible, setCollaborationVisible] = useState(false)
  const [sessionId, setSessionId] = useState('default-session')
  const [fileContent, setFileContent] = useState('')
  const [language, setLanguage] = useState('python')

  const handleFileClick = (file) => {
    if (file.type === 'file') {
      setActiveFile(file)
      
      // Tab aç veya mevcut tab'a git
      const existingTab = openTabs.find(tab => tab.id === file.id)
      if (existingTab) {
        setActiveTab(existingTab.id)
      } else {
        const newTab = { ...file }
        setOpenTabs([...openTabs, newTab])
        setActiveTab(newTab.id)
      }

      // Dosya içeriğini yükle
      loadFileContent(file.path)
    }
  }

  const handleTabClose = (tabId, e) => {
    e.stopPropagation()
    const newTabs = openTabs.filter(tab => tab.id !== tabId)
    setOpenTabs(newTabs)
    
    if (activeTab === tabId) {
      setActiveTab(newTabs.length > 0 ? newTabs[newTabs.length - 1].id : null)
      setActiveFile(newTabs.length > 0 ? newTabs[newTabs.length - 1] : null)
    }
  }

  const handleTabClick = (tab) => {
    setActiveTab(tab.id)
    setActiveFile(tab)
    loadFileContent(tab.path)
  }

  const loadFileContent = async (path) => {
    try {
      const response = await fetch(`/api/editor/file?path=${encodeURIComponent(path)}`)
      if (response.ok) {
        const data = await response.json()
        setFileContent(data.content || `# ${path}\n# Content loaded from backend`)
      } else {
        setFileContent(`# ${path}\n# Failed to load content`)
      }
    } catch (error) {
      setFileContent(`# ${path}\n# Error loading content`)
    }

    // Dil belirle
    if (path.endsWith('.py')) setLanguage('python')
    else if (path.endsWith('.js')) setLanguage('javascript')
    else if (path.endsWith('.jsx')) setLanguage('javascript')
    else if (path.endsWith('.ts')) setLanguage('typescript')
    else if (path.endsWith('.tsx')) setLanguage('typescript')
    else if (path.endsWith('.html')) setLanguage('html')
    else if (path.endsWith('.css')) setLanguage('css')
    else if (path.endsWith('.json')) setLanguage('json')
    else setLanguage('plaintext')
  }

  const handleContentChange = (newContent) => {
    setFileContent(newContent)
  }

  return (
    <div className="app">
      <div className="app-container">
        {/* Sidebar - File Tree */}
        <div className="sidebar">
          <FileTree 
            onFileClick={handleFileClick}
            activeFile={activeFile}
          />
        </div>

        {/* Main Editor Area */}
        <div className="main-editor">
          {/* Tabs */}
          <div className="editor-tabs">
            {openTabs.map(tab => (
              <div 
                key={tab.id} 
                className={`tab ${activeTab === tab.id ? 'active' : ''}`}
                onClick={() => handleTabClick(tab)}
              >
                <span>{tab.name}</span>
                <span 
                  className="tab-close"
                  onClick={(e) => handleTabClose(tab.id, e)}
                >
                  ×
                </span>
              </div>
            ))}
          </div>

          {/* Monaco Editor */}
          <div className="monaco-container">
            {activeFile ? (
              <Editor
                content={fileContent}
                language={language}
                onChange={handleContentChange}
                filePath={activeFile.path}
              />
            ) : (
              <div className="editor-placeholder">
                <div className="placeholder-icon">
                  <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                    <polyline points="10 9 9 9 8 9"></polyline>
                  </svg>
                </div>
                <div className="placeholder-text">
                  <h2>MuhammedAI Local Developer</h2>
                  <p>Select a file to start editing</p>
                </div>
              </div>
            )}
          </div>

          {/* Terminal Panel */}
          {terminalVisible && (
            <Terminal 
              onClose={() => setTerminalVisible(false)}
            />
          )}
        </div>

        {/* AI Panel */}
        {aiPanelVisible && (
          <AIPanel 
            onClose={() => setAiPanelVisible(false)}
          />
        )}

        {/* Debugger Panel */}
        {debuggerVisible && (
          <Debugger 
            onClose={() => setDebuggerVisible(false)}
          />
        )}

        {/* Collaboration Panel */}
        {collaborationVisible && (
          <Collaboration 
            isOpen={collaborationVisible}
            onClose={() => setCollaborationVisible(false)}
            sessionId={sessionId}
          />
        )}
      </div>

      {/* Status Bar */}
      <StatusBar 
        onToggleTerminal={() => setTerminalVisible(!terminalVisible)}
        onToggleAI={() => setAiPanelVisible(!aiPanelVisible)}
        onToggleDebugger={() => setDebuggerVisible(!debuggerVisible)}
        onToggleCollaboration={() => setCollaborationVisible(!collaborationVisible)}
        terminalVisible={terminalVisible}
        aiPanelVisible={aiPanelVisible}
        debuggerVisible={debuggerVisible}
        collaborationVisible={collaborationVisible}
        activeFile={activeFile}
      />
    </div>
  )
}

export default App
