import React, { useState } from 'react';
import StepIndicator     from './components/StepIndicator';
import FileUploader      from './components/FileUploader';
import DataSummary       from './components/DataSummary';
import ColumnSelector    from './components/ColumnSelector';
import TaskSelector      from './components/TaskSelector';
import ProgressBar       from './components/ProgressBar';
import ROCChart          from './components/ROCChart';
import RegressionChart   from './components/RegressionChart';
import ClusteringChart   from './components/ClusteringChart';
import SessionHistory    from './components/SessionHistory';
import './App.css';

const STEP_TITLES = [
  'Upload Data',
  'Preview & Clean',
  'Select Columns',
  'Choose Task',
  'Run Model'
];

export default function App() {
  const [step, setStep]           = useState(1);
  const [sessionId, setSessionId] = useState(localStorage.getItem('sessionId') || '');
  const [fileName, setFileName]   = useState('');
  const [columns, setColumns]     = useState([]);
  const [preview, setPreview]     = useState([]);
  const [summary, setSummary]     = useState({});
  const [selection, setSelection] = useState({ features: [], target: '' });
  const [task, setTask]           = useState('');
  const [hyperparams, setHyperparams] = useState({});
  const [progress, setProgress]   = useState(0);
  const [result, setResult]       = useState(null);
  const [activeTimestamp, setActiveTimestamp] = useState(null);

  // STEP 1 → 2: upload & fetch summary
  const handleUpload = async data => {
    setSessionId(data.session_id);
    setFileName(data.filename);
    localStorage.setItem('sessionId', data.session_id);

    setColumns(data.columns);
    setPreview(data.preview);
    setStep(2);

    const res = await fetch(`http://localhost:8000/summary/${data.session_id}`);
    const json = await res.json();
    setSummary(json.summary);
  };

  // STEP 2 → 3: cleaned columns
  const handleClean = cleanedColumns => {
    setColumns(cleanedColumns);
    setStep(3);
  };

  // STEP 3 → 4: column selection
  const handleColumns = sel => {
    setSelection(sel);
    setStep(4);
  };

  // STEP 4 → 5: task + hyperparams
  const handleTask = params => {
    setTask(params.task);
    setHyperparams(params.hyperparams);
    setStep(5);
  };

  // STEP 5: start training
  const handleRun = () => {
    setProgress(0);
    setResult(null);

    const ws = new WebSocket('ws://localhost:8000/ws/train/');
    ws.onopen = () => {
      ws.send(JSON.stringify({
        session_id: sessionId,
        features: selection.features,
        target: selection.target,
        task,
        hyperparams
      }));
    };
    ws.onmessage = e => {
      const msg = JSON.parse(e.data);
      if (msg.progress !== undefined) setProgress(msg.progress);
      if (msg.error) alert(msg.error);
      if (msg.result) setResult(msg.result);
      if (msg.snapshot) setActiveTimestamp(msg.snapshot.timestamp);
    };
  };

  // Load a past snapshot into view
  const handleSelectSnapshot = snap => {
    setTask(snap.task);
    setResult(snap.result);
    setActiveTimestamp(snap.timestamp);
    setStep(5);
  };

  return (
    <div className="app-root">
      {/* Top banner */}
      <div className="banner">
        <div className="banner-title">ML Web App</div>
        <div className="banner-file">{fileName || 'No file selected'}</div>
      </div>

      {/* Sidebar + Main */}
      <div className="app-container">
        {/* Sidebar */}
        <div className="sidebar">
          <h2>Session History</h2>
          <SessionHistory
            sessionId={sessionId}
            onSelect={handleSelectSnapshot}
            activeTimestamp={activeTimestamp}
          />
        </div>

        {/* Main panel */}
        <div className="main-content">
          <div className="card">
            <div className="card-body">
              <StepIndicator current={step} />
              <h2 className="content-title">{STEP_TITLES[step - 1]}</h2>

              {step === 1 && (
                <FileUploader onUpload={handleUpload} />
              )}

              {step === 2 && (
                <DataSummary
                  columns={columns}
                  summary={summary}
                  onNext={handleClean}
                />
              )}

              {step === 3 && (
                <ColumnSelector
                  columns={columns}
                  preview={preview}
                  onNext={handleColumns}
                />
              )}

              {step === 4 && (
                <TaskSelector onNext={handleTask} />
              )}

              {step === 5 && (
                <>
                  <button className="btn" onClick={handleRun}>
                    Start Training
                  </button>

                  {progress > 0 && (
                    <div className="progress-container">
                      <ProgressBar percent={progress} />
                    </div>
                  )}

                  {result && (
                    <div className="result">
                      {task === 'classification' && result.fpr && (
                        <ROCChart fpr={result.fpr} tpr={result.tpr} />
                      )}
                      {task === 'regression' && result.actual && (
                        <RegressionChart
                          actual={result.actual}
                          predicted={result.predicted}
                        />
                      )}
                      {task === 'clustering' && result.data && (
                        <ClusteringChart
                          data={result.data}
                          centers={result.centers}
                        />
                      )}
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
