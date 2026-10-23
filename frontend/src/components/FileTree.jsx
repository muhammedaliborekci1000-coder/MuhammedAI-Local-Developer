import React, { useState, useEffect } from 'react'
import { File, Folder, FolderOpen, ChevronRight, ChevronDown, RefreshCw } from 'lucide-react'

const FileTree = ({ onFileClick, activeFile }) => {
  const [files, setFiles] = useState([])
  const [loading, setLoading] = useState(true)
  const [currentPath, setCurrentPath] = useState('')

  useEffect(() => {
    loadFiles('')
  }, [])

  const loadFiles = async (path) => {
    setLoading(true)
    try {
      const response = await fetch(`/api/editor/files?path=${encodeURIComponent(path)}`)
      const data = await response.json()
      if (data.success) {
        setCurrentPath(data.path)
        // API'den gelen items'ı tree structure'a çevir
        const treeItems = data.items.map(item => ({
          id: item.path,
          name: item.name,
          type: item.type,
          path: item.path,
          expanded: false,
          children: item.type === 'folder' ? [] : null
        }))
        setFiles(treeItems)
      }
    } catch (error) {
      console.error('Failed to load files:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFolderClick = async (file) => {
    // Folder toggle
    const toggleFolder = (items) => {
      return items.map(item => {
        if (item.id === file.id) {
          const newExpanded = !item.expanded
          if (newExpanded && item.children && item.children.length === 0) {
            // Load children
            loadFiles(file.path)
          }
          return { ...item, expanded: newExpanded }
        }
        if (item.children) {
          return { ...item, children: toggleFolder(item.children) }
        }
        return item
      })
    }
    setFiles(toggleFolder(files))
  }

  const renderFile = (file, level = 0) => {
    const paddingLeft = level * 12 + 10
    const isActive = activeFile && activeFile.id === file.id

    if (file.type === 'folder') {
      return (
        <div key={file.id}>
          <div
            className="file-item"
            style={{ paddingLeft }}
            onClick={() => handleFolderClick(file)}
          >
            {file.expanded ? (
              <ChevronDown size={12} className="file-icon" />
            ) : (
              <ChevronRight size={12} className="file-icon" />
            )}
            {file.expanded ? (
              <FolderOpen size={16} className="file-icon" />
            ) : (
              <Folder size={16} className="file-icon" />
            )}
            <span>{file.name}</span>
          </div>
          {file.expanded && file.children && (
            <div>
              {file.children.map(child => renderFile(child, level + 1))}
            </div>
          )}
        </div>
      )
    } else {
      return (
        <div
          key={file.id}
          className={`file-item ${isActive ? 'active' : ''}`}
          style={{ paddingLeft }}
          onClick={() => onFileClick(file)}
        >
          <File size={16} className="file-icon" />
          <span>{file.name}</span>
        </div>
      )
    }
  }

  return (
    <div className="file-tree">
      <div className="file-tree-header">
        <span>Explorer</span>
        <button onClick={() => loadFiles(currentPath)} className="refresh-btn">
          <RefreshCw size={14} />
        </button>
      </div>
      {loading ? (
        <div className="file-tree-loading">Loading...</div>
      ) : (
        files.map(file => renderFile(file))
      )}
    </div>
  )
}

export default FileTree
