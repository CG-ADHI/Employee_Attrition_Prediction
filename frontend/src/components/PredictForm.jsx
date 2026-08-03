import React, { useState, useRef } from 'react';

/* ── Risk Ring SVG ── */
const RiskRing = ({ probability = 0, riskLevel = 'LOW' }) => {
  const radius = 52;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (probability / 100) * circumference;
  const colorClass =
    riskLevel === 'HIGH'   ? 'risk-ring-fill-high' :
    riskLevel === 'MEDIUM' ? 'risk-ring-fill-medium' : 'risk-ring-fill-low';
  const color =
    riskLevel === 'HIGH'   ? '#F43F5E' :
    riskLevel === 'MEDIUM' ? '#F59E0B' : '#10B981';

  return (
    <div className="risk-ring">
      <svg viewBox="0 0 120 120">
        <circle cx="60" cy="60" r={radius} fill="none" strokeWidth="10" className="risk-ring-bg" />
        <circle
          cx="60" cy="60" r={radius} fill="none" strokeWidth="10"
          className={`risk-ring-fill ${colorClass}`}
          stroke={color}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
        />
      </svg>
      <div className="risk-ring-label">
        <span style={{ fontSize: '1.4rem', fontWeight: 800, fontFamily: "'Space Grotesk', sans-serif", color }}>
          {probability.toFixed(0)}%
        </span>
        <span style={{ fontSize: '0.65rem', color: 'var(--text-3)', fontWeight: 600, letterSpacing: '0.08em', textTransform: 'uppercase' }}>
          Risk
        </span>
      </div>
    </div>
  );
};

/* ── Slider Field ── */
const SliderField = ({ label, name, min, max, value, onChange, step = 1 }) => (
  <div className="form-group">
    <label>{label}</label>
    <div className="slider-wrapper">
      <input
        type="range" name={name} min={min} max={max} step={step}
        value={value}
        onChange={e => onChange(name, Number(e.target.value))}
      />
      <span className="slider-value">{value}</span>
    </div>
  </div>
);

/* ── Select Field ── */
const SelectField = ({ label, name, value, onChange, options }) => (
  <div className="form-group">
    <label>{label}</label>
    <select name={name} className="form-control" value={value} onChange={e => onChange(name, e.target.value)}>
      {options.map(o => <option key={o} value={o}>{o}</option>)}
    </select>
  </div>
);

const INITIAL = {
  Age: 32, Department: 'Research & Development', Gender: 'Male',
  MonthlyIncome: 5000, OverTime: 'No', YearsAtCompany: 5,
  WorkLifeBalance: 3, JobSatisfaction: 3, DistanceFromHome: 10,
  JobRole: 'Research Scientist', BusinessTravel: 'Travel_Rarely',
  Education: 3, EducationField: 'Life Sciences',
  EnvironmentSatisfaction: 3, JobInvolvement: 3, JobLevel: 2,
  MaritalStatus: 'Single', NumCompaniesWorked: 1,
  PercentSalaryHike: 14, PerformanceRating: 3,
  RelationshipSatisfaction: 3, StockOptionLevel: 0,
  TotalWorkingYears: 8, TrainingTimesLastYear: 3,
  YearsInCurrentRole: 4, YearsSinceLastPromotion: 1,
  YearsWithCurrManager: 3,
};

const RISK_FACTORS_MAP = {
  OverTime:       v => v === 'Yes' ? 'Working overtime' : null,
  JobSatisfaction: v => v <= 2 ? 'Low job satisfaction (≤ 2)' : null,
  MonthlyIncome:  v => v < 3000 ? 'Below-average compensation' : null,
  YearsAtCompany: v => v < 3 ? 'Short tenure (< 3 years)' : null,
  DistanceFromHome: v => v > 20 ? `Long commute (${v} km)` : null,
  WorkLifeBalance: v => v <= 2 ? 'Poor work-life balance (≤ 2)' : null,
  EnvironmentSatisfaction: v => v <= 2 ? 'Low environment satisfaction' : null,
  MaritalStatus:  v => v === 'Single' ? 'Single (higher mobility)' : null,
};

const TABS = ['Personal', 'Job & Satisfaction', 'Experience'];

const PredictForm = () => {
  const [data, setData] = useState(INITIAL);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [tab, setTab] = useState(0);
  const resultRef = useRef(null);

  const update = (name, value) => setData(p => ({ ...p, [name]: value }));
  const handleInput = e => {
    const { name, value, type } = e.target;
    update(name, type === 'number' ? Number(value) : value);
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true); setError(null); setResult(null);
    try {
      const res = await fetch('http://localhost:8000/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Server error');
      }
      const json = await res.json();
      setResult(json);
      setTimeout(() => resultRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 100);
    } catch (err) {
      setError(err.message || 'Failed to connect to the prediction server.');
    }
    setLoading(false);
  };

  const riskFactors = Object.entries(RISK_FACTORS_MAP)
    .map(([k, fn]) => fn(data[k]))
    .filter(Boolean);

  const probability = result ? parseFloat((result.probability * 100).toFixed(1)) : 0;
  const riskLevel   = result?.risk_level || 'LOW';

  return (
    <div className="grid grid-2 gap-6">
      {/* ── Form Panel ── */}
      <div className="card card-lg">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 style={{ marginBottom: '0.2rem' }}>Employee Profile</h3>
            <p className="text-muted text-sm">Fill in the employee details below</p>
          </div>
          <span className="badge badge-purple">ML Powered</span>
        </div>

        {/* Tabs */}
        <div className="tabs">
          {TABS.map((t, i) => (
            <button key={i} className={`tab-btn ${tab === i ? 'active' : ''}`} onClick={() => setTab(i)}>
              {t}
            </button>
          ))}
        </div>

        <form onSubmit={handleSubmit}>
          {/* Tab 0 — Personal */}
          {tab === 0 && (
            <div className="grid grid-2 gap-4">
              <div className="form-group">
                <label>Age</label>
                <input type="number" name="Age" className="form-control" value={data.Age}
                  onChange={handleInput} min="18" max="65" />
              </div>
              <SelectField label="Gender" name="Gender" value={data.Gender} onChange={update}
                options={['Male', 'Female']} />
              <SelectField label="Marital Status" name="MaritalStatus" value={data.MaritalStatus} onChange={update}
                options={['Single', 'Married', 'Divorced']} />
              <div className="form-group">
                <label>Distance From Home (km)</label>
                <input type="number" name="DistanceFromHome" className="form-control"
                  value={data.DistanceFromHome} onChange={handleInput} min="1" max="100" />
              </div>
              <SelectField label="Education Field" name="EducationField" value={data.EducationField} onChange={update}
                options={['Life Sciences', 'Medical', 'Marketing', 'Technical Degree', 'Human Resources', 'Other']} />
              <SliderField label="Education Level (1–5)" name="Education" min={1} max={5}
                value={data.Education} onChange={update} />
            </div>
          )}

          {/* Tab 1 — Job & Satisfaction */}
          {tab === 1 && (
            <div className="grid grid-2 gap-4">
              <SelectField label="Department" name="Department" value={data.Department} onChange={update}
                options={['Sales', 'Research & Development', 'Human Resources']} />
              <SelectField label="Job Role" name="JobRole" value={data.JobRole} onChange={update}
                options={['Sales Executive', 'Research Scientist', 'Laboratory Technician', 'Manager',
                  'Healthcare Representative', 'Manufacturing Director', 'Sales Representative',
                  'Research Director', 'Human Resources']} />
              <SelectField label="Business Travel" name="BusinessTravel" value={data.BusinessTravel} onChange={update}
                options={['Non-Travel', 'Travel_Rarely', 'Travel_Frequently']} />
              <SelectField label="OverTime" name="OverTime" value={data.OverTime} onChange={update}
                options={['No', 'Yes']} />
              <div className="form-group">
                <label>Monthly Income (₹)</label>
                <input type="number" name="MonthlyIncome" className="form-control"
                  value={data.MonthlyIncome} onChange={handleInput} min="1000" />
              </div>
              <SliderField label="Job Level (1–5)" name="JobLevel" min={1} max={5}
                value={data.JobLevel} onChange={update} />
              <SliderField label="Job Satisfaction (1–4)" name="JobSatisfaction" min={1} max={4}
                value={data.JobSatisfaction} onChange={update} />
              <SliderField label="Job Involvement (1–4)" name="JobInvolvement" min={1} max={4}
                value={data.JobInvolvement} onChange={update} />
              <SliderField label="Work-Life Balance (1–4)" name="WorkLifeBalance" min={1} max={4}
                value={data.WorkLifeBalance} onChange={update} />
              <SliderField label="Environment Satisfaction (1–4)" name="EnvironmentSatisfaction" min={1} max={4}
                value={data.EnvironmentSatisfaction} onChange={update} />
            </div>
          )}

          {/* Tab 2 — Experience */}
          {tab === 2 && (
            <div className="grid grid-2 gap-4">
              <div className="form-group">
                <label>Total Working Years</label>
                <input type="number" name="TotalWorkingYears" className="form-control"
                  value={data.TotalWorkingYears} onChange={handleInput} min="0" max="40" />
              </div>
              <div className="form-group">
                <label>Years at Company</label>
                <input type="number" name="YearsAtCompany" className="form-control"
                  value={data.YearsAtCompany} onChange={handleInput} min="0" max="40" />
              </div>
              <div className="form-group">
                <label>Years in Current Role</label>
                <input type="number" name="YearsInCurrentRole" className="form-control"
                  value={data.YearsInCurrentRole} onChange={handleInput} min="0" max="20" />
              </div>
              <div className="form-group">
                <label>Years Since Last Promotion</label>
                <input type="number" name="YearsSinceLastPromotion" className="form-control"
                  value={data.YearsSinceLastPromotion} onChange={handleInput} min="0" max="20" />
              </div>
              <div className="form-group">
                <label>Years with Current Manager</label>
                <input type="number" name="YearsWithCurrManager" className="form-control"
                  value={data.YearsWithCurrManager} onChange={handleInput} min="0" max="20" />
              </div>
              <div className="form-group">
                <label>Companies Worked Before</label>
                <input type="number" name="NumCompaniesWorked" className="form-control"
                  value={data.NumCompaniesWorked} onChange={handleInput} min="0" max="10" />
              </div>
              <SliderField label="Stock Option Level (0–3)" name="StockOptionLevel" min={0} max={3}
                value={data.StockOptionLevel} onChange={update} />
              <SliderField label="Training Times Last Year (0–6)" name="TrainingTimesLastYear" min={0} max={6}
                value={data.TrainingTimesLastYear} onChange={update} />
              <SliderField label="Performance Rating (1–4)" name="PerformanceRating" min={1} max={4}
                value={data.PerformanceRating} onChange={update} />
              <SliderField label="Percent Salary Hike" name="PercentSalaryHike" min={11} max={25}
                value={data.PercentSalaryHike} onChange={update} />
            </div>
          )}

          {/* Nav + Submit */}
          <div className="flex justify-between gap-3 mt-6">
            <button type="button" className="btn btn-ghost" disabled={tab === 0} onClick={() => setTab(t => t - 1)}>
              ← Back
            </button>
            {tab < TABS.length - 1 ? (
              <button type="button" className="btn btn-secondary" onClick={() => setTab(t => t + 1)}>
                Next →
              </button>
            ) : (
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? <><div className="spinner" style={{ width: 16, height: 16 }} /> Analyzing…</> : '🔍 Run Prediction'}
              </button>
            )}
          </div>
        </form>
      </div>

      {/* ── Results Panel ── */}
      <div className="flex flex-col gap-4" ref={resultRef}>
        {/* Pre-assessment risk scan */}
        {!result && (
          <div className="card">
            <div className="section-title mb-3">Live Risk Scan</div>
            <p className="text-muted text-sm mb-4">
              Based on the current profile values, the following risk signals are detected:
            </p>
            {riskFactors.length > 0 ? (
              <div>
                {riskFactors.map((f, i) => (
                  <div key={i} className="risk-factor-item">
                    <div className="risk-factor-dot" style={{ background: 'var(--warning)' }} />
                    <span style={{ fontSize: '0.825rem', color: 'var(--text-2)' }}>{f}</span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-state" style={{ padding: '1.5rem' }}>
                <span style={{ fontSize: '1.5rem' }}>✅</span>
                <p className="text-muted text-sm">No immediate risk signals detected in current profile.</p>
              </div>
            )}
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="card animate-in" style={{ borderLeft: '3px solid var(--danger)' }}>
            <div className="flex items-center gap-3 mb-2">
              <span>⚠️</span>
              <span style={{ fontWeight: 600, color: 'var(--danger)' }}>Prediction Failed</span>
            </div>
            <p className="text-muted text-sm">{error}</p>
            <p className="text-muted text-sm mt-2">
              Make sure the FastAPI backend is running on port 8000.
            </p>
          </div>
        )}

        {/* Result Card */}
        {result && (
          <div className="card card-lg animate-in">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 style={{ marginBottom: '0.25rem' }}>Prediction Result</h3>
                <p className="text-muted text-sm">Machine learning attrition analysis</p>
              </div>
              <span className={`badge ${
                riskLevel === 'HIGH' ? 'badge-red' :
                riskLevel === 'MEDIUM' ? 'badge-amber' : 'badge-green'
              }`} style={{ fontSize: '0.8rem', padding: '0.35rem 0.85rem' }}>
                {riskLevel} RISK
              </span>
            </div>

            {/* Ring + Status */}
            <div className="flex items-center gap-6 mb-6">
              <RiskRing probability={probability} riskLevel={riskLevel} />
              <div style={{ flex: 1 }}>
                <div style={{ marginBottom: '0.5rem' }}>
                  <span className="text-muted text-sm">Verdict</span>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '0.15rem' }}>
                    {result.prediction === 1 ? '🔴 Likely to Leave' : '🟢 Likely to Stay'}
                  </div>
                </div>
                <div style={{ marginBottom: '0.5rem' }}>
                  <span className="text-muted text-sm">Attrition Probability</span>
                  <div style={{ fontWeight: 700, color: probability > 50 ? 'var(--danger)' : 'var(--success)', fontSize: '1.3rem', fontFamily: "'Space Grotesk', sans-serif" }}>
                    {probability}%
                  </div>
                </div>
                <div className="progress-bar" style={{ height: 8 }}>
                  <div
                    className="progress-fill"
                    style={{
                      width: `${probability}%`,
                      background: riskLevel === 'HIGH' ? '#F43F5E' : riskLevel === 'MEDIUM' ? '#F59E0B' : '#10B981',
                    }}
                  />
                </div>
              </div>
            </div>

            <div className="divider" />

            {/* Risk Factors */}
            <div>
              <div className="section-title mb-3">Identified Risk Factors</div>
              {riskFactors.length > 0 ? (
                riskFactors.map((f, i) => (
                  <div key={i} className="risk-factor-item">
                    <div className="risk-factor-dot" style={{ background: 'var(--danger)' }} />
                    <span style={{ fontSize: '0.825rem', color: 'var(--text-2)' }}>{f}</span>
                  </div>
                ))
              ) : (
                <p className="text-muted text-sm">No specific risk flags in profile data.</p>
              )}
            </div>

            {result.prediction === 1 && (
              <>
                <div className="divider" />
                <div style={{
                  background: 'var(--danger-bg)',
                  border: '1px solid var(--danger-border)',
                  borderRadius: 'var(--r-md)',
                  padding: '0.875rem 1rem',
                }}>
                  <span style={{ fontWeight: 600, color: 'var(--danger)', fontSize: '0.85rem' }}>
                    ⚡ Recommended Action
                  </span>
                  <p style={{ fontSize: '0.8rem', color: 'var(--text-2)', marginTop: '0.4rem', lineHeight: 1.6 }}>
                    Schedule a 1-on-1 retention conversation. Consider compensation review, 
                    role enrichment, or flexible work options.
                  </p>
                </div>
              </>
            )}
          </div>
        )}

        {/* Model Info */}
        <div className="card card-sm" style={{ borderLeft: '3px solid var(--brand-purple)' }}>
          <div className="section-title mb-2" style={{ fontSize: '0.8rem' }}>About This Model</div>
          <div className="insight-row">
            <span className="insight-label">Algorithm</span>
            <span className="insight-value">Random Forest (RF)</span>
          </div>
          <div className="insight-row">
            <span className="insight-label">Accuracy</span>
            <span className="insight-value text-green">84.0%</span>
          </div>
          <div className="insight-row">
            <span className="insight-label">Training Records</span>
            <span className="insight-value">1,176</span>
          </div>
          <div className="insight-row">
            <span className="insight-label">Features Used</span>
            <span className="insight-value">35</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictForm;
