import React from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip
} from 'recharts';

export default function ROCChart({ fpr, tpr }) {
  const data = fpr.map((x, i) => ({ fpr: x, tpr: tpr[i] }));
  return (
    <div style={{ marginTop: '1rem' }}>
      <h4>ROC Curve</h4>
      <LineChart width={500} height={300} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="fpr" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="tpr" stroke="#8884d8" dot={false} />
      </LineChart>
    </div>
  );
}
