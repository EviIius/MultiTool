import React, { useState, useEffect } from 'react';
import '../App.css';

export default function SessionHistory({ sessionId, onSelect, activeTimestamp }) {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (!sessionId) return;
    fetch(`http://localhost:8000/history/${sessionId}`)
      .then(r => r.json())
      .then(data => setHistory(data));
  }, [sessionId]);

  return (
    <div className="session-history">
      {history.map((snap, i) => (
        <div
          key={i}
          className={`session-item${snap.timestamp === activeTimestamp ? ' active' : ''}`}
          onClick={() => onSelect(snap)}
        >
          <div className="session-item-title">{snap.task}</div>
          <div className="session-item-time">
            {new Date(snap.timestamp).toLocaleString()}
          </div>
        </div>
      ))}
    </div>
  );
}
