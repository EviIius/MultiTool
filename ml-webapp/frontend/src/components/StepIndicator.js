import React from 'react';
import '../App.css';

const labels = ['Upload', 'Columns', 'Task', 'Train'];

export default function StepIndicator({ current }) {
  return (
    <div className="stepper">
      {labels.map((label, i) => (
        <div key={i} className={`step ${current === i + 1 ? 'active' : ''}`}>
          <div className="step-number">{i + 1}</div>
          <div className="step-label">{label}</div>
        </div>
      ))}
    </div>
  );
}
