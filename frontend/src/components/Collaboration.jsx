import React, { useState, useEffect, useRef } from 'react';
import { Users, MessageSquare, Share2, X } from 'lucide-react';

const Collaboration = ({ isOpen, onClose, sessionId }) => {
  const [connected, setConnected] = useState(false);
  const [users, setUsers] = useState([]);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [cursors, setCursors] = useState({});
  const wsRef = useRef(null);

  useEffect(() => {
    if (isOpen && sessionId) {
      connectWebSocket();
    } else {
      disconnectWebSocket();
    }

    return () => {
      disconnectWebSocket();
    };
  }, [isOpen, sessionId]);

  const connectWebSocket = () => {
    const ws = new WebSocket(`ws://localhost:8000/ws/collaboration/${sessionId}`);
    wsRef.current = ws;

    ws.onopen = () => {
      setConnected(true);
      console.log('Connected to collaboration session');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'cursor') {
        setCursors(prev => ({
          ...prev,
          [data.userId]: { position: data.position, color: data.color }
        }));
      } else if (data.type === 'edit') {
        // Handle edit
        console.log('Edit received:', data);
      } else if (data.type === 'message') {
        setMessages(prev => [...prev, data]);
      } else if (data.type === 'user_joined') {
        setUsers(prev => [...prev, data.user]);
      } else if (data.type === 'user_left') {
        setUsers(prev => prev.filter(u => u.id !== data.userId));
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setConnected(false);
    };

    ws.onclose = () => {
      setConnected(false);
      console.log('Disconnected from collaboration session');
    };
  };

  const disconnectWebSocket = () => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setConnected(false);
  };

  const sendMessage = () => {
    if (inputMessage.trim() && wsRef.current) {
      wsRef.current.send(JSON.stringify({
        type: 'message',
        content: inputMessage,
        timestamp: new Date().toISOString()
      }));
      setInputMessage('');
    }
  };

  const shareSession = () => {
    const shareUrl = `${window.location.origin}?session=${sessionId}`;
    navigator.clipboard.writeText(shareUrl);
    alert('Session link copied to clipboard!');
  };

  if (!isOpen) return null;

  return (
    <div className="collaboration-panel">
      <div className="collaboration-header">
        <div className="collaboration-title">
          <Users size={18} />
          <span>Collaboration</span>
        </div>
        <div className="collaboration-actions">
          <button 
            className="collaboration-btn"
            onClick={shareSession}
            title="Share session"
          >
            <Share2 size={16} />
          </button>
          <button 
            className="collaboration-btn"
            onClick={onClose}
            title="Close"
          >
            <X size={16} />
          </button>
        </div>
      </div>

      <div className="collaboration-content">
        <div className="collaboration-status">
          <div className={`status-indicator ${connected ? 'connected' : 'disconnected'}`}></div>
          <span>{connected ? 'Connected' : 'Disconnected'}</span>
        </div>

        <div className="collaboration-users">
          <div className="users-header">
            <Users size={16} />
            <span>Users ({users.length})</span>
          </div>
          <div className="users-list">
            {users.map(user => (
              <div key={user.id} className="user-item">
                <div 
                  className="user-avatar"
                  style={{ backgroundColor: user.color }}
                >
                  {user.name.charAt(0).toUpperCase()}
                </div>
                <span className="user-name">{user.name}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="collaboration-chat">
          <div className="chat-header">
            <MessageSquare size={16} />
            <span>Chat</span>
          </div>
          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className="chat-message">
                <div className="message-sender">{msg.sender}</div>
                <div className="message-content">{msg.content}</div>
              </div>
            ))}
          </div>
          <div className="chat-input">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Type a message..."
              disabled={!connected}
            />
            <button 
              onClick={sendMessage}
              disabled={!connected || !inputMessage.trim()}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Collaboration;
