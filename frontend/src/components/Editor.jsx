import React, { useRef, useEffect, useState } from 'react'
import Editor from '@monaco-editor/react'

const CodeEditor = ({ content, language, onChange, filePath }) => {
  const editorRef = useRef(null)
  const [aiSuggestions, setAiSuggestions] = useState([])
  const [showAiSuggestion, setShowAiSuggestion] = useState(false)

  const handleEditorDidMount = (editor, monaco) => {
    editorRef.current = editor
    
    // VS Code dark theme
    monaco.editor.defineTheme('vs-dark-custom', {
      base: 'vs-dark',
      inherit: true,
      rules: [],
      colors: {
        'editor.background': '#1e1e1e',
        'editor.foreground': '#d4d4d4',
        'editorCursor.foreground': '#aeafad',
        'editor.lineHighlightBackground': '#2a2d2e',
        'editorLineNumber.foreground': '#858585',
        'editor.selectionBackground': '#264f78',
        'editor.inactiveSelectionBackground': '#3a3d41',
      }
    })
    monaco.editor.setTheme('vs-dark-custom')
    
    // AI-powered completion provider with context awareness
    monaco.languages.registerCompletionItemProvider('python', {
      async provideCompletionItems(model, position) {
        const word = model.getWordUntilPosition(position)
        const range = {
          startLineNumber: position.lineNumber,
          endLineNumber: position.lineNumber,
          startColumn: word.startColumn,
          endColumn: word.endColumn
        }
        
        // Get code context
        const code = model.getValue()
        const line = position.lineNumber
        const column = position.column
        
        // Get surrounding context (previous lines)
        const contextLines = []
        const startLine = Math.max(0, line - 5)
        for (let i = startLine; i < line; i++) {
          contextLines.push(model.getLineContent(i + 1))
        }
        const context = contextLines.join('\n')
        
        try {
          // Try context-aware AI completion first
          const response = await fetch('/api/editor/intellisense/context-complete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              file_path: filePath || '',
              code: code,
              line: line,
              column: column,
              context: context
            })
          })
          const data = await response.json()
          
          if (data.success && data.completions && data.completions.length > 0) {
            return {
              suggestions: data.completions.map(comp => ({
                label: comp.label,
                kind: comp.type === 'ai-context' ? monaco.languages.CompletionItemKind.Snippet : monaco.languages.CompletionItemKind.Text,
                detail: comp.detail,
                insertText: comp.label,
                range: range
              }))
            }
          }
        } catch (error) {
          console.error('Context-aware completion failed:', error)
        }
        
        // Fallback to LSP completion
        try {
          const lspResponse = await fetch('/api/editor/lsp/completion', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              file_path: filePath || '',
              code: code,
              line: line,
              column: column
            })
          })
          const lspData = await lspResponse.json()
          
          if (lspData.success && lspData.completions) {
            return {
              suggestions: lspData.completions.map(comp => ({
                label: comp.label,
                kind: comp.kind || monaco.languages.CompletionItemKind.Text,
                detail: comp.detail,
                insertText: comp.label,
                range: range
              }))
            }
          }
        } catch (error) {
          console.error('LSP completion failed:', error)
        }
        
        // Fallback to empty suggestions
        return { suggestions: [] }
      }
    })
    
    // Hover provider
    monaco.languages.registerHoverProvider('python', {
      async provideHover(model, position) {
        try {
          const response = await fetch('/api/editor/lsp/hover', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              file_path: filePath || '',
              code: model.getValue(),
              line: position.lineNumber,
              column: position.column
            })
          })
          const data = await response.json()
          
          if (data.success && data.hover) {
            return {
              range: new monaco.Range(
                data.hover.range.start.line,
                data.hover.range.start.character,
                data.hover.range.end.line,
                data.hover.range.end.character
              ),
              contents: [{ value: data.hover.contents }]
            }
          }
        } catch (error) {
          console.error('Hover failed:', error)
        }
        return null
      }
    })
    
    // Definition provider (go-to-definition)
    monaco.languages.registerDefinitionProvider('python', {
      async provideDefinition(model, position) {
        try {
          const response = await fetch('/api/editor/lsp/definition', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              file_path: filePath || '',
              code: model.getValue(),
              line: position.lineNumber,
              column: position.column
            })
          })
          const data = await response.json()
          
          if (data.success && data.definition) {
            return [
              new monaco.Uri(data.definition.uri),
              new monaco.Range(
                data.definition.range.start.line,
                data.definition.range.start.character,
                data.definition.range.end.line,
                data.definition.range.end.character
              )
            ]
          }
        } catch (error) {
          console.error('Definition failed:', error)
        }
        return []
      }
    })
  }

  const handleEditorChange = (value) => {
    onChange(value)
  }

  return (
    <div className="editor-wrapper">
      <Editor
        height="100%"
        language={language}
        value={content}
        onChange={handleEditorChange}
        onMount={handleEditorDidMount}
        theme="vs-dark-custom"
        options={{
          minimap: { enabled: true },
          fontSize: 14,
          lineNumbers: 'on',
          roundedSelection: false,
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 4,
          wordWrap: 'on',
          formatOnPaste: true,
          formatOnType: true,
          autoClosingBrackets: 'always',
          autoClosingQuotes: 'always',
          autoIndent: 'full',
          suggestOnTriggerCharacters: true,
          quickSuggestions: {
            other: true,
            comments: false,
            strings: false
          },
          parameterHints: { enabled: true },
          folding: true,
          foldingStrategy: 'auto',
          showFoldingControls: 'always',
          matchBrackets: 'always',
          bracketPairColorization: { enabled: true },
          guides: {
            bracketPairs: true,
            indentation: true
          },
          renderWhitespace: 'selection',
          renderLineHighlight: 'all',
          cursorBlinking: 'smooth',
          cursorSmoothCaretAnimation: 'on',
          smoothScrolling: true,
          mouseWheelZoom: true,
          contextmenu: true,
          suggest: {
            showKeywords: true,
            showSnippets: true,
          },
        }}
      />
    </div>
  )
}

export default CodeEditor
