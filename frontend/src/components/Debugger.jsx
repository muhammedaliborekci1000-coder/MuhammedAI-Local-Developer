import React, { useState, useEffect } from 'react'
import { X, Play, Pause, StepOver, StepInto, StepOut, Bug, Square, ChevronDown, ChevronUp, RefreshCw } from 'lucide-react'

const Debugger = ({ onClose }) => {
  const [session, setSession] = useState(null)
  const [breakpoints, setBreakpoints] = useState([])
  const [variables, setVariables] = useState([])
  const [stack, setStack] = useState([])
  const [collapsed, setCollapsed] = useState(false)
  const [currentLine, setCurrentLine] = useState(null)
  const [debuggerState, setDebuggerState] = useState('idle')
  const [loading, setLoading] = useState(false)

  // Poll debugger state every second
  useEffect(() => {
    if (session) {
      const interval = setInterval(pollDebuggerState, 1000)
      return () => clearInterval(interval)
    }
  }, [session])

  const pollDebuggerState = async () => {
    try {
      const response = await fetch('/api/editor/debugger/state')
      const data = await response.json()
      if (data.success) {
        setDebuggerState(data.state)
        if (data.current_frame) {
          setCurrentLine(data.current_frame.line)
        }
        setBreakpoints(data.breakpoints || [])
      }
    } catch (error) {
      console.error('Failed to poll debugger state:', error)
    }
  }

  const startDebugger = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/editor/debugger/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: 'main.py' })
      })
      const data = await response.json()
      if (data.success) {
        setSession(data)
        setDebuggerState('running')
      }
    } catch (error) {
      console.error('Failed to start debugger:', error)
    } finally {
      setLoading(false)
    }
  }

  const stopDebugger = async () => {
    if (!session) return
    setLoading(true)
    try {
      await fetch('/api/editor/debugger/stop', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: session.session_id })
      })
      setSession(null)
      setBreakpoints([])
      setVariables([])
      setStack([])
      setDebuggerState('idle')
      setCurrentLine(null)
    } catch (error) {
      console.error('Failed to stop debugger:', error)
    } finally {
      setLoading(false)
    }
  }

  const addBreakpoint = async (line) => {
    setLoading(true)
    try {
      await fetch('/api/editor/debugger/breakpoint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: session?.session_id,
          file_path: session?.file_path,
          line: line,
          action: 'add'
        })
      })
      pollDebuggerState()
    } catch (error) {
      console.error('Failed to add breakpoint:', error)
    } finally {
      setLoading(false)
    }
  }

  const removeBreakpoint = async (line) => {
    setLoading(true)
    try {
      await fetch('/api/editor/debugger/breakpoint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: session?.session_id,
          file_path: session?.file_path,
          line: line,
          action: 'remove'
        })
      })
      pollDebuggerState()
    } catch (error) {
      console.error('Failed to remove breakpoint:', error)
    } finally {
      setLoading(false)
    }
  }

  const step = async (action) => {
    if (!session) return
    setLoading(true)
    try {
      await fetch('/api/editor/debugger/step', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: session.session_id,
          action: action
        })
      })
      // Wait a bit then poll for updates
      setTimeout(() => {
        pollDebuggerState()
        fetchVariables()
        fetchStack()
      }, 500)
    } catch (error) {
      console.error('Failed to step:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchVariables = async () => {
    if (!session) return
    try {
      const response = await fetch(`/api/editor/debugger/variables?session_id=${session.session_id}`)
      const data = await response.json()
      if (data.success) {
        setVariables(data.variables || [])
      }
    } catch (error) {
      console.error('Failed to fetch variables:', error)
    }
  }

  const fetchStack = async () => {
    if (!session) return
    try {
      const response = await fetch(`/api/editor/debugger/stack?session_id=${session.session_id}`)
      const data = await response.json()
      if (data.success) {
        setStack(data.stack || [])
      }
    } catch (error) {
      console.error('Failed to fetch stack:', error)
    }
  }

  const isPaused = debuggerState === 'paused'
  const isRunning = debuggerState === 'running'

  return (
    <div className={`debugger-panel ${collapsed ? 'collapsed' : ''}`}>
      <div className="debugger-header">
        <div className="debugger-title">
          <Bug size={14} />
          <span>Debugger</span>
          {session && (
            <span className={`debugger-status ${debuggerState}`}>
              {debuggerState}
            </span>
          )}
        </div>
        <div className="debugger-controls">
          <button onClick={() => pollDebuggerState()} className="debugger-btn" title="Refresh">
            <RefreshCw size={14} />
          </button>
          <button onClick={() => setCollapsed(!collapsed)} className="debugger-btn">
            {collapsed ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
          </button>
          <button onClick={onClose} className="debugger-btn">
            <X size={14} />
          </button>
        </div>
      </div>

      {!collapsed && (
        <div className="debugger-content">
          {!session ? (
            <div className="debugger-empty">
              <button onClick={startDebugger} className="debugger-start-btn" disabled={loading}>
                {loading ? <span className="loading-spinner"></span> : <Play size={16} />}
                Start Debugging
              </button>
            </div>
          ) : (
            <>
              {/* Debugger Controls */}
              <div className="debugger-toolbar">
                <button 
                  onClick={() => step('continue')} 
                  className="debugger-tool-btn" 
                  title="Continue"
                  disabled={loading || !isPaused}
                >
                  <Play size={16} />
                </button>
                <button 
                  onClick={() => step('over')} 
                  className="debugger-tool-btn" 
                  title="Step Over"
                  disabled={loading || !isPaused}
                >
                  <StepOver size={16} />
                </button>
                <button 
                  onClick={() => step('into')} 
                  className="debugger-tool-btn" 
                  title="Step Into"
                  disabled={loading || !isPaused}
                >
                  <StepInto size={16} />
                </button>
                <button 
                  onClick={() => step('out')} 
                  className="debugger-tool-btn" 
                  title="Step Out"
                  disabled={loading || !isPaused}
                >
                  <StepOut size={16} />
                </button>
                <button 
                  onClick={stopDebugger} 
                  className="debugger-tool-btn stop" 
                  title="Stop"
                  disabled={loading}
                >
                  <Square size={16} />
                </button>
              </div>

              {/* Current Position */}
              {currentLine && (
                <div className="debugger-section">
                  <div className="debugger-section-title">Current Position</div>
                  <div className="debugger-current-position">
                    Line {currentLine}
                  </div>
                </div>
              )}

              {/* Breakpoints */}
              <div className="debugger-section">
                <div className="debugger-section-title">Breakpoints</div>
                <div className="debugger-breakpoints">
                  {breakpoints.length === 0 ? (
                    <div className="debugger-empty-text">No breakpoints</div>
                  ) : (
                    breakpoints.map((bp, index) => (
                      <div key={index} className="debugger-breakpoint">
                        <span>{bp.file}:{bp.line}</span>
                        <button 
                          onClick={() => removeBreakpoint(bp.line)} 
                          className="debugger-remove-btn"
                          disabled={loading}
                        >
                          ×
                        </button>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* Variables */}
              <div className="debugger-section">
                <div className="debugger-section-title">Variables</div>
                <div className="debugger-variables">
                  {variables.length === 0 ? (
                    <div className="debugger-empty-text">No variables</div>
                  ) : (
                    variables.map((variable, index) => (
                      <div key={index} className="debugger-variable">
                        <span className="variable-name">{variable.name}</span>
                        <span className="variable-value">{variable.value}</span>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* Stack Trace */}
              <div className="debugger-section">
                <div className="debugger-section-title">Call Stack</div>
                <div className="debugger-stack">
                  {stack.length === 0 ? (
                    <div className="debugger-empty-text">No stack frames</div>
                  ) : (
                    stack.map((frame, index) => (
                      <div key={index} className="debugger-stack-frame">
                        <span>{frame.function}</span>
                        <span className="stack-location">{frame.file}:{frame.line}</span>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  )
}

export default Debugger
