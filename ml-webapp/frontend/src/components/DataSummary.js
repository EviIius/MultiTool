import React, { useState } from 'react';
import '../App.css';

export default function DataSummary({ columns, summary, onNext }) {
  const [dropped, setDropped] = useState([]);

  const toggleDrop = col => {
    setDropped(d => d.includes(col) ? d.filter(x=>x!==col) : [...d, col]);
  };

  const cleaned = columns.filter(c => !dropped.includes(c));

  return (
    <div>
      <table className="data-preview">
        <thead>
          <tr>
            <th>Column</th><th>Type</th><th>Count</th><th>Nulls</th><th>Unique</th>
          </tr>
        </thead>
        <tbody>
          {columns.map(col=>(
            <tr key={col} className={dropped.includes(col) ? 'muted' : ''}>
              <td>
                <input
                  type="checkbox"
                  checked={!dropped.includes(col)}
                  onChange={()=>toggleDrop(col)}
                />{' '}
                {col}
              </td>
              <td>{summary[col]?.dtype}</td>
              <td>{summary[col]?.count}</td>
              <td>{summary[col]?.nulls}</td>
              <td>{summary[col]?.unique}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <button
        className="btn"
        onClick={()=>onNext(cleaned)}
        disabled={cleaned.length===0}
      >
        Next → Select Columns
      </button>
    </div>
  );
}
