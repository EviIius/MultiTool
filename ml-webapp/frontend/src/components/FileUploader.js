import React from 'react';

export default function FileUploader({ onUpload }) {
  const handleChange = async e => {
    const file = e.target.files[0];
    if (!file) return;
    const form = new FormData();
    form.append('file', file);

    const res = await fetch('http://localhost:8000/upload/', {
      method: 'POST',
      body: form
    });
    const data = await res.json();
    // pass filename along for banner
    onUpload({ ...data, filename: file.name });
  };

  return (
    <div className="form-group">
      <input type="file" accept=".csv, .xls, .xlsx, .json" onChange={handleChange} />
    </div>
  );
}
