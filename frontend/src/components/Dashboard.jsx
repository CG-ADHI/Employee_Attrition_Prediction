import React, { useEffect, useState } from 'react';
import { API_BASE_URL } from '../config';
import {
  AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';

/* ── Static data (representative of IBM HR dataset) ── */
const ATTRITION_TREND = [
  { month: 'Jan', rate: 14.2 }, { month: 'Feb', rate: 15.8 },
  { month: 'Mar', rate: 13.6 }, { month: 'Apr', rate: 16.2 },
  { month: 'May', rate: 15.0 }, { month: 'Jun', rate: 17.1 },
  { month: 'Jul', rate: 16.1 }, { month: 'Aug', rate: 15.4 },
];

const DEPT_BREAKDOWN = [
  { dept: 'Sales',  risk: 20.6, count: 92 },
  { dept: 'R&D',    risk: 13.8, count: 133 },
  { dept: 'HR',     risk: 19.0, count: 12 },
];

const RISK_DIST = [
  { name: 'Low Risk',    value: 62, color: '#10B981' },
  { name: 'Medium Risk', value: 22, color: '#F59E0B' },
  { name: 'High Risk',   value: 16, color: '#F43F5E' },
];

const TOP_FACTORS = [
  { name: 'OverTime',             pct: 31, color: '#F43F5E' },
  { name: 'Job Satisfaction',     pct: 27, color: '#F59E0B' },
  { name: 'Distance from Home',   pct: 22, color: '#A78BFA' },
  { name: 'Monthly Income',       pct: 18, color: '#22D3EE' },
  { name: 'Years at Company',     pct: 14, color: '#4F8EF7' },
];

/* ── Custom Tooltip ── */
const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: 'var(--surface-3)',
      border: '1px solid var(--border-2)',
      borderRadius: 'var(--r-md)',
      padding: '0.625rem 1rem',
      fontSize: '0.8rem',
      boxShadow: 'var(--shadow-md)',
    }}>
      <p style={{ color: 'var(--text-2)', marginBottom: '0.25rem' }}>{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.color || p.fill || 'var(--text-1)', fontWeight: 600 }}>
          {p.name}: {p.value}{p.name === 'rate' ? '%' : ''}
        </p>
      ))}
    </div>
  );
};

/* ── KPI Card ── */
const KpiCard = ({ title, value, sub, iconBg, icon, deltaType, delta }) => (
  <div className="card stagger">
    <div className="card-header">
      <div>
        <div className="card-title">{title}</div>
        <div className="card-value">{value}</div>
        {delta && (
          <span className={`stat-delta ${deltaType === 'up' ? 'stat-delta-up' : 'stat-delta-down'}`}>
            {deltaType === 'up' ? '↑' : '↓'} {delta}
          </span>
        )}
      </div>
      <div className={`card-icon ${iconBg}`} style={{ fontSize: '1.25rem' }}>{icon}</div>
    </div>
    {sub && <div className="card-sub">{sub}</div>}
  </div>
);

const Dashboard = () => {
  const [metrics, setMetrics] = useState({ total_employees: 1470, features: 35, models_deployed: 3 });

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/dashboard`)
      .then(r => r.json())
      .then(d => { if (!d.error) setMetrics(d); })
      .catch(() => {});
  }, []);

  return (
    <div>
      {/* KPIs */}
      <div className="grid grid-4 mb-6 stagger">
        <KpiCard
          title="Total Employees"
          value={metrics.total_employees.toLocaleString()}
          sub="Across all departments"
          iconBg="card-icon-blue"
          icon="👥"
          deltaType="up" delta="2.4% this quarter"
        />
        <KpiCard
          title="Attrition Rate"
          value="16.1%"
          sub="Current trailing 12 months"
          iconBg="card-icon-rose"
          icon="📉"
          deltaType="down" delta="1.2% vs last year"
        />
        <KpiCard
          title="High Risk Employees"
          value="236"
          sub="Probability > 60%"
          iconBg="card-icon-amber"
          icon="⚠️"
          deltaType="down" delta="18 resolved"
        />
        <KpiCard
          title="Model Accuracy"
          value="84.0%"
          sub="Random Forest classifier"
          iconBg="card-icon-green"
          icon="🤖"
          deltaType="up" delta="vs 75% baseline"
        />
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-2 mb-6">
        {/* Attrition Trend */}
        <div className="card">
          <div className="card-header">
            <div>
              <div className="section-title">Attrition Rate Trend</div>
              <div className="card-sub">Monthly attrition % — 2024</div>
            </div>
            <span className="badge badge-blue">Live</span>
          </div>
          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={ATTRITION_TREND} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="gradBlue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="#4F8EF7" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#4F8EF7" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="month" stroke="var(--text-4)" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis stroke="var(--text-4)" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={v => `${v}%`} />
                <Tooltip content={<CustomTooltip />} />
                <Area type="monotone" dataKey="rate" name="rate" stroke="#4F8EF7" strokeWidth={2.5}
                  fill="url(#gradBlue)" dot={{ fill: '#4F8EF7', r: 3 }} activeDot={{ r: 5, strokeWidth: 0 }} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Distribution Pie */}
        <div className="card flex flex-col">
          <div className="card-header">
            <div>
              <div className="section-title">Risk Distribution</div>
              <div className="card-sub">Employee attrition risk bands</div>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', flex: 1 }}>
            <div style={{ width: 180, height: 180, flexShrink: 0 }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={RISK_DIST} cx="50%" cy="50%" innerRadius={50} outerRadius={80}
                    paddingAngle={3} dataKey="value" strokeWidth={0}>
                    {RISK_DIST.map((d, i) => <Cell key={i} fill={d.color} />)}
                  </Pie>
                  <Tooltip content={<CustomTooltip />} />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div style={{ flex: 1 }}>
              {RISK_DIST.map(d => (
                <div key={d.name} style={{ marginBottom: '0.75rem' }}>
                  <div className="flex justify-between mb-1">
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-2)', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                      <span style={{ width: 8, height: 8, borderRadius: '50%', background: d.color, display: 'inline-block' }} />
                      {d.name}
                    </span>
                    <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-1)' }}>{d.value}%</span>
                  </div>
                  <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${d.value}%`, background: d.color }} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-2 mb-6">
        {/* Dept Risk */}
        <div className="card">
          <div className="card-header">
            <div>
              <div className="section-title">Department Risk Rate</div>
              <div className="card-sub">Attrition % by department</div>
            </div>
          </div>
          <div className="chart-wrapper-short">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={DEPT_BREAKDOWN} layout="vertical" margin={{ top: 0, right: 20, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={false} />
                <XAxis type="number" stroke="var(--text-4)" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={v => `${v}%`} />
                <YAxis type="category" dataKey="dept" stroke="var(--text-4)" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} width={45} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="risk" name="Attrition %" fill="#4F8EF7" radius={[0, 4, 4, 0]} barSize={22}>
                  {DEPT_BREAKDOWN.map((_, i) => {
                    const colors = ['#F43F5E', '#4F8EF7', '#F59E0B'];
                    return <Cell key={i} fill={colors[i]} />;
                  })}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top Risk Factors */}
        <div className="card">
          <div className="card-header">
            <div>
              <div className="section-title">Top Attrition Drivers</div>
              <div className="card-sub">Feature importance from Random Forest</div>
            </div>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            {TOP_FACTORS.map((f, i) => (
              <div key={i}>
                <div className="flex justify-between mb-1">
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-2)' }}>{f.name}</span>
                  <span style={{ fontSize: '0.78rem', fontWeight: 700, color: f.color }}>{f.pct}%</span>
                </div>
                <div className="progress-bar">
                  <div className="progress-fill" style={{ width: `${f.pct}%`, background: f.color, transition: `width ${0.5 + i * 0.1}s ease` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Info Row */}
      <div className="card" style={{ borderLeft: '3px solid var(--brand-blue)' }}>
        <div className="flex items-center gap-3">
          <span style={{ fontSize: '1.25rem' }}>💡</span>
          <div>
            <span style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-1)' }}>
              Insight: Sales department carries the highest attrition risk at 20.6%.
            </span>
            <span style={{ fontSize: '0.825rem', color: 'var(--text-3)', marginLeft: '0.5rem' }}>
              Top contributing factor is OverTime — 31% of high-risk employees work excessive hours.
              Use the Predictor to assess individual employees.
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
