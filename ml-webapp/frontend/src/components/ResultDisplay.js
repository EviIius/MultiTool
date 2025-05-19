// src/components/ResultDisplay.js
import React from 'react';

export default function ResultDisplay({ result }) {
  if (!result) return null;
  return (
    <div className="result">
      <h3>3. Results</h3>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}
