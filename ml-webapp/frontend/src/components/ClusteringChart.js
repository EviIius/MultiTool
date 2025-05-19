import React from 'react';
import {
  ResponsiveContainer, ScatterChart, Scatter, XAxis,
  YAxis, CartesianGrid, Tooltip, Legend
} from 'recharts';

export default function ClusteringChart({ data, centers }) {
  const clusters = Array.from(new Set(data.map(d => d.cluster)));

  return (
    <div style={{ marginTop: '1.5rem', width: '100%', height: 400 }}>
      <h4>Cluster Scatter (first two features)</h4>
      <ResponsiveContainer width="100%" height="100%">
        <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
          <CartesianGrid />
          <XAxis dataKey="x" name="Feature 1" />
          <YAxis dataKey="y" name="Feature 2" />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} />
          <Legend />
          {clusters.map(c => (
            <Scatter
              key={c}
              name={`Cluster ${c}`}
              data={data.filter(d => d.cluster === c)}
            />
          ))}
          <Scatter name="Centers" data={centers} fill="#000" shape="star" />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}
