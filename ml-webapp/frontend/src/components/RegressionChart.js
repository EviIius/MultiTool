import React from 'react';
import {
  ResponsiveContainer, ScatterChart, Scatter, XAxis,
  YAxis, CartesianGrid, Tooltip, ReferenceLine
} from 'recharts';

export default function RegressionChart({ actual, predicted }) {
  const data = actual.map((a, i) => ({
    actual: a,
    predicted: predicted[i]
  }));

  return (
    <div style={{ marginTop: '1.5rem', width: '100%', height: 400 }}>
      <h4>Actual vs. Predicted</h4>
      <ResponsiveContainer width="100%" height="100%">
        <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
          <CartesianGrid />
          <XAxis dataKey="actual" name="Actual" />
          <YAxis dataKey="predicted" name="Predicted" />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} />
          <Scatter name="Data points" data={data} fill="#8884d8" />
          <ReferenceLine x={0} y={0} stroke="#000" label="y = x" />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}
