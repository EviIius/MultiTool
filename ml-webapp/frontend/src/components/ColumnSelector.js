import React, { useState } from 'react';
import '../App.css';

export default function ColumnSelector({ columns, preview, onNext }) {
  const [features, setFeatures] = useState([]);
  const [target, setTarget]     = useState('');

  const toggleFeature = col => {
    setFeatures(prev =>
      prev.includes(col)
        ? prev.filter(f => f !== col)
        : [...prev, col]
    );
  };

  return (
    <div>
      <table className="data-preview">
        <thead>
          <tr>{columns.map(c => <th key={c}>{c}</th>)}</tr>
        </thead>
        <tbody>
          {preview.map((row, i) => (
            <tr key={i}>
              {columns.map(c => <td key={c}>{row[c]}</td>)}
            </tr>
          ))}
        </tbody>
      </table>

      <div className="form-group">
        <label>Features</label>
        <div className="form-group-checkbox">
          {columns.map(col => (
            <label key={col}>
              <input
                type="checkbox"
                value={col}
                checked={features.includes(col)}
                onChange={() => toggleFeature(col)}
              />
              {col}
            </label>
          ))}
        </div>
      </div>

      <div className="form-group">
        <label>Target</label>
        <select value={target} onChange={e => setTarget(e.target.value)}>
          <option value="">— none —</option>
          {columns.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
      </div>

      <button
        className="btn"
        disabled={features.length === 0}
        onClick={() => onNext({ features, target })}
      >
        Next → Task
      </button>
    </div>
  );
}
