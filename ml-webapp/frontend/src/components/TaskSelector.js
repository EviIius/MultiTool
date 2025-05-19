import React, { useEffect, useState } from 'react';

export default function TaskSelector({ onNext }) {
  const [meta, setMeta] = useState({});
  const [task, setTask] = useState('');
  const [hp, setHp]     = useState({});

  useEffect(() => {
    fetch('http://localhost:8000/tasks/')
      .then(r => r.json())
      .then(d => setMeta(d));
  }, []);

  const onChangeHP = (key, val) =>
    setHp(h => ({ ...h, [key]: Number(val) || val }));

  return (
    <div>
      <div className="form-group">
        <label>Task</label>
        <select
          value={task}
          onChange={e => {
            setTask(e.target.value);
            setHp({});
          }}
        >
          <option value="">— choose —</option>
          {Object.entries(meta).map(
            ([k, v]) => <option key={k} value={k}>{v.label}</option>
          )}
        </select>
      </div>

      {task && meta[task].hyperparams && Object.entries(meta[task].hyperparams).map(
        ([key, cfg]) => (
          <div className="form-group" key={key}>
            <label>{cfg.label}</label>
            <input
              type="number"
              min={cfg.min}
              max={cfg.max}
              value={hp[key] ?? cfg.default}
              onChange={e => onChangeHP(key, e.target.value)}
            />
          </div>
        )
      )}

      <button
        className="btn"
        disabled={!task}
        onClick={() => onNext({ task, hyperparams: hp })}
      >
        Next → Run
      </button>
    </div>
  );
}
