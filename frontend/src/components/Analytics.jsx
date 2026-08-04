import React, { useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell, LineChart, Line, RadarChart,
  PolarGrid, PolarAngleAxis, Radar, Legend
} from 'recharts';

const CT = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: 'var(--surface-3)', border: '1px solid var(--border-2)',
      borderRadius: 'var(--r-md)', padding: '0.625rem 1rem',
      fontSize: '0.8rem', boxShadow: 'var(--shadow-md)',
    }}>
      <p style={{ color: 'var(--text-3)', marginBottom: '0.25rem', fontSize: '0.75rem' }}>{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.fill || p.stroke || 'var(--text-1)', fontWeight: 600 }}>
          {p.name}: {typeof p.value === 'number' ? p.value.toFixed(1) : p.value}
          {p.name?.includes('%') || p.name?.includes('rate') ? '%' : ''}
        </p>
      ))}
    </div>
  );
};

/* ── Data ── */
const DEPT_DATA = [
  { dept: 'Sales',  stayed: 354, left: 92,  rate: 20.6 },
  { dept: 'R&D',    stayed: 828, left: 133, rate: 13.8 },
  { dept: 'HR',     stayed: 51,  left: 12,  rate: 19.0 },
];

const SATISFACTION = [
  { rating: '1 — Low', attrition: 66, stayed: 200 },
  { rating: '2',       attrition: 46, stayed: 280 },
  { rating: '3',       attrition: 73, stayed: 422 },
  { rating: '4 — High',attrition: 52, stayed: 331 },
];

const OVERTIME_DATA = [
  { name: 'No Overtime',  rate: 10.4, employees: 1054 },
  { name: 'Works OT',     rate: 30.5, employees: 416 },
];

const INCOME_BANDS = [
  { band: '< ₹3k',   rate: 32, n: 148 },
  { band: '₹3–5k',   rate: 21, n: 312 },
  { band: '₹5–8k',   rate: 14, n: 396 },
  { band: '₹8–12k',  rate: 9,  n: 290 },
  { band: '> ₹12k',  rate: 5,  n: 324 },
];

const TENURE_DATA = [
  { years: '0–1', rate: 38 }, { years: '2–3', rate: 22 },
  { years: '4–5', rate: 16 }, { years: '6–9', rate: 11 },
  { years: '10+', rate: 8 },
];

const RADAR_DATA = [
  { subject: 'Job Satisfaction',    A: 70, B: 30 },
  { subject: 'Work-Life Balance',   A: 65, B: 45 },
  { subject: 'Env Satisfaction',    A: 72, B: 28 },
  { subject: 'Relationship Sat.',   A: 68, B: 40 },
  { subject: 'Job Involvement',     A: 75, B: 35 },
];

const ROLE_ATTRITION = [
  { role: 'Sales Rep',         rate: 39.8 },
  { role: 'Lab Technician',    rate: 23.9 },
  { role: 'HR',                rate: 23.1 },
  { role: 'Sales Executive',   rate: 17.5 },
  { role: 'Research Scientist',rate: 16.1 },
  { role: 'Manufacturing Dir.',rate: 6.9  },
  { role: 'Healthcare Rep.',   rate: 7.7  },
  { role: 'Manager',           rate: 5.0  },
  { role: 'Research Director', rate: 2.5  },
];

const BAR_COLORS = ['#F43F5E','#F59E0B','#4F8EF7','#10B981','#A78BFA','#22D3EE','#F97316','#6366F1','#EC4899'];

const Analytics = () => {
  const [chartView, setChartView] = useState('count'); // 'count' | 'rate'

  return (
    <div>
      {/* Header strip */}
      <div className="card mb-6" style={{ background: 'linear-gradient(135deg, rgba(79,142,247,0.08) 0%, rgba(34,211,238,0.05) 100%)', borderColor: 'var(--border-accent)' }}>
        <div className="flex items-center justify-between">
          <div>
            <h3 style={{ marginBottom: '0.25rem' }}>Workforce Analytics</h3>
            <p className="text-muted text-sm">Exploratory data analysis based on IBM HR dataset — 1,470 employees</p>
          </div>
          <div className="flex gap-2">
            <span className="badge badge-blue">1,233 Stayed</span>
            <span className="badge badge-red">237 Left</span>
            <span className="badge badge-amber">16.1% Rate</span>
          </div>
        </div>
      </div>

      {/* Row 1: Dept Attrition + Overtime Impact */}
      <div className="grid grid-2 mb-6">
        {/* Dept Attrition */}
        <div className="card">
          <div className="card-header">
            <div>
              <div className="section-title">Attrition by Department</div>
              <div className="card-sub">Stayed vs Left counts</div>
            </div>
            <div className="tabs" style={{ marginBottom: 0, padding: '0.15rem' }}>
              {['count', 'rate'].map(v => (
                <button key={v} className={`tab-btn ${chartView === v ? 'active' : ''}`}
                  style={{ flex: 'none', padding: '0.25rem 0.65rem', fontSize: '0.72rem' }}
                  onClick={() => setChartView(v)}>
                  {v === 'count' ? 'Count' : 'Rate%'}
                </button>
              ))}
            </div>
          </div>
          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height="100%">
              {chartView === 'count' ? (
                <BarChart data={DEPT_DATA} margin={{ top: 5, right: 10, left: -15, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.05)" vertical={false} />
                  <XAxis dataKey="dept" stroke="var(--text-4)" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis stroke="var(--text-4)" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
                  <Tooltip content={<CT />} />
                  <Legend iconSize={10} iconType="circle" wrapperStyle={{ fontSize: '0.75rem' }} />
                  <Bar dataKey="stayed" name="Stayed" fill="#2563EB" radius={[4, 4, 0, 0]} barSize={30} />
                  <Bar dataKey="left"   name="Left"   fill="#EF4444" radius={[4, 4, 0, 0]} barSize={30} />
                </BarChart>
              ) : (
                <BarChart data={DEPT_DATA} margin={{ top: 5, right: 10, left: -15, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.05)" vertical={false} />
                  <XAxis dataKey="dept" stroke="var(--text-4)" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis stroke="var(--text-4)" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={v => `${v}%`} domain={[0, 30]} />
                  <Tooltip content={<CT />} />
                  <Bar dataKey="rate" name="Attrition %" radius={[4, 4, 0, 0]} barSize={36}>
                    {DEPT_DATA.map((_, i) => <Cell key={i} fill={BAR_COLORS[i]} />)}
                  </Bar>
                </BarChart>
              )}
            </ResponsiveContainer>
          </div>
        </div>

        {/* Overtime Impact */}
        <div className="card flex flex-col justify-between">
          <div>
            <div className="card-header">
              <div>
                <div className="section-title">OverTime Impact</div>
                <div className="card-sub">Attrition rate: overtime vs non-overtime</div>
              </div>
              <span className="badge badge-red">High Correlation</span>
            </div>
            <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem' }}>
              {OVERTIME_DATA.map((d, i) => (
                <div key={i} style={{
                  flex: 1, background: 'var(--surface-3)', borderRadius: 'var(--r-lg)',
                  padding: '1.25rem', border: '1px solid var(--border-1)', textAlign: 'center'
                }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-3)', marginBottom: '0.5rem', fontWeight: 600 }}>
                    {d.name}
                  </div>
                  <div style={{
                    fontSize: '2rem', fontFamily: "'Space Grotesk', sans-serif", fontWeight: 800,
                    color: d.rate > 20 ? 'var(--danger)' : 'var(--success)'
                  }}>
                    {d.rate}%
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-3)', marginTop: '0.35rem' }}>
                    {d.employees.toLocaleString()} employees
                  </div>
                  <div className="progress-bar mt-2">
                    <div className="progress-fill" style={{
                      width: `${d.rate * 2}%`,
                      background: d.rate > 20 ? 'var(--danger)' : 'var(--success)'
                    }} />
                  </div>
                </div>
              ))}
            </div>
          </div>
          <p className="text-muted text-sm mt-4" style={{ lineHeight: 1.6 }}>
            ⚡ Employees working overtime have a <strong style={{ color: 'var(--danger)' }}>3× higher attrition rate</strong> than those who don't.
            This is the single strongest predictor in the model.
          </p>
        </div>
      </div>

      {/* Row 2: Job Role Attrition + Income Attrition */}
      <div className="grid grid-2 mb-6">
        {/* Job Role */}
        <div className="card">
          <div className="card-header">
            <div>
              <div className="section-title">Attrition Rate by Job Role</div>
              <div className="card-sub">Ranked from highest to lowest attrition rate</div>
            </div>
          </div>
          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={ROLE_ATTRITION.slice().sort((a, b) => b.rate - a.rate)}
                layout="vertical"
                margin={{ top: 0, right: 20, left: 10, bottom: 0 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.05)" horizontal={false} vertical={true} />
                <XAxis type="number" stroke="var(--text-4)" tick={{ fontSize: 10 }} axisLine={false} tickLine={false} tickFormatter={v => `${v}%`} domain={[0, 45]} />
                <YAxis type="category" dataKey="role" stroke="var(--text-4)" tick={{ fontSize: 9 }} axisLine={false} tickLine={false} width={110} />
                <Tooltip content={<CT />} />
                <Bar dataKey="rate" name="Attrition %" radius={[0, 4, 4, 0]} barSize={12}>
                  {ROLE_ATTRITION.slice().sort((a, b) => b.rate - a.rate).map((d, i) => (
                    <Cell key={i} fill={d.rate > 25 ? 'var(--danger)' : d.rate > 15 ? 'var(--warning)' : 'var(--brand-blue)'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Income vs Attrition */}
        <div className="card">
          <div className="card-header">
            <div>
              <div className="section-title">Monthly Income vs Attrition</div>
              <div className="card-sub">Attrition rate by income band</div>
            </div>
          </div>
          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={INCOME_BANDS} margin={{ top: 5, right: 10, left: -15, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.05)" vertical={false} />
                <XAxis dataKey="band" stroke="var(--text-4)" tick={{ fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis stroke="var(--text-4)" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={v => `${v}%`} />
                <Tooltip content={<CT />} />
                <Line type="monotone" dataKey="rate" name="Attrition %" stroke="#F59E0B" strokeWidth={2.5}
                  dot={{ fill: '#F59E0B', r: 5 }} activeDot={{ r: 7, strokeWidth: 0 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Key Insights */}
      <div className="card" style={{ borderLeft: '3px solid var(--brand-cyan)' }}>
        <div className="section-title mb-3">📌 Key Findings</div>
        <div className="grid grid-3 gap-4">
          {[
            { icon: '⚡', color: 'var(--danger)', text: 'OverTime workers leave 3× more than non-OT employees (30.5% vs 10.4%)' },
            { icon: '💼', color: 'var(--warning)', text: 'Sales Representatives have the highest attrition (39.8%) among all roles' },
            { icon: '💰', color: 'var(--success)', text: 'Income below ₹3k/month correlates with 32% attrition — 6× more than > ₹12k' },
          ].map((item, i) => (
            <div key={i} style={{ background: 'var(--surface-3)', borderRadius: 'var(--r-md)', padding: '1rem', border: '1px solid var(--border-1)' }}>
              <span style={{ fontSize: '1.25rem' }}>{item.icon}</span>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-2)', marginTop: '0.5rem', lineHeight: 1.6 }}>{item.text}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Analytics;
