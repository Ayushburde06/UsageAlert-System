import { useState, useEffect, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [data, setData] = useState([]);
  const [stats, setStats] = useState(null);
  const fileInputRef = useRef(null);

  const API_URL = 'https://usagealert-system.onrender.com'; // Target FastAPI endpoint on Render

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a supported file first.');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to upload and process file.');
      }

      await fetchAnomalies();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchAnomalies = async () => {
    try {
      const response = await fetch(`${API_URL}/anomalies`);
      if (!response.ok) throw new Error('Failed to fetch anomalies');
      
      const result = await response.json();
      setData(result.data);
      setStats(result.stats);
    } catch (err) {
      setError(err.message);
    }
  };

  // Custom dot for recharts to highlight anomalies in red
  const CustomDot = (props) => {
    const { cx, cy, payload } = props;
    if (payload.is_forecast) {
      return null; // forecast doesn't need dots
    }
    if (payload.is_anomaly) {
      return (
        <circle cx={cx} cy={cy} r={4} fill="#ef4444" stroke="none" />
      );
    }
    return null;
  };

  return (
    <div className="dashboard">
      <header className="header">
        <h1>AI Energy Anomaly Detection</h1>
        <p>Upload telemetry data to detect energy usage outliers</p>
      </header>

      <section className="upload-section">
        <input 
          type="file" 
          accept=".csv,.xlsx,.xls" 
          onChange={handleFileChange} 
          ref={fileInputRef}
          className="file-input"
          id="file-upload"
        />
        <label htmlFor="file-upload" className="file-label">
          {file ? file.name : 'Click to select a file (CSV, Excel)'}
        </label>
        <div>
          <button 
            className="btn" 
            onClick={handleUpload}
            disabled={!file || loading}
          >
            {loading ? <><span className="spinner"></span> Analyzing...</> : 'Upload & Detect'}
          </button>
        </div>
        {error && <div className="error">{error}</div>}
      </section>

      {stats && (
        <>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Readings</h3>
              <p className="value">{stats.total_readings}</p>
            </div>
            <div className="stat-card">
              <h3>Anomalies Detected</h3>
              <p className="value anomaly">{stats.anomaly_count}</p>
            </div>
            <div className="stat-card">
              <h3>Avg Energy Usage</h3>
              <p className="value">{stats.avg_energy.toFixed(2)}</p>
            </div>
          </div>

          <div className="chart-section">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="time" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#3b82f6" 
                  name="Energy Usage"
                  dot={<CustomDot />}
                  activeDot={{ r: 6 }}
                  strokeWidth={2}
                />
                <Line 
                  type="monotone" 
                  dataKey="forecast_value" 
                  stroke="#10b981" 
                  name="Forecasted Usage"
                  strokeDasharray="5 5"
                  strokeWidth={2}
                  dot={false}
                  activeDot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
