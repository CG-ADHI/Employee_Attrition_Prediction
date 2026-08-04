import React, { useState } from 'react';
import './index.css';
import Dashboard   from './components/Dashboard';
import PredictForm from './components/PredictForm';
import Analytics   from './components/Analytics';
import Watchlist   from './components/Watchlist';

/* ── SVG Icon helpers ─────────────────────── */
const Icon = ({ d, size = 18 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
       stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round">
    <path d={d} />
  </svg>
);

const ICONS = {
  dashboard: 'M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z M9 22V12h6v10',
  predict:   'M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2 M12 11a4 4 0 100-8 4 4 0 000 8z',
  analytics: 'M18 20V10 M12 20V4 M6 20v-6',
  watchlist: 'M9 11l3 3L22 4 M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11',
  logout:    'M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4 M16 17l5-5-5-5 M21 12H9',
};

const PAGE_META = {
  dashboard: { title: 'Dashboard',          subtitle: 'Overview of your workforce analytics' },
  predict:   { title: 'Employee Predictor', subtitle: 'Assess individual attrition risk' },
  analytics: { title: 'Analytics',          subtitle: 'Trends and workforce distribution insights' },
  watchlist: { title: 'Risk Watchlist',     subtitle: 'At-risk employee management' },
};

function App() {
  const [activeTab, setActiveTab]   = useState('dashboard');

  const meta = PAGE_META[activeTab];

  return (
    <div className="app-shell">
      {/* ══ SIDEBAR ══════════════════════════════ */}
      <aside className="sidebar">
        {/* Brand */}
        <div className="sidebar-brand">
          <div className="sidebar-brand-icon">📊</div>
          <div className="sidebar-brand-text">
            <span className="sidebar-brand-title">PeopleIQ</span>
            <span className="sidebar-brand-sub">HR Analytics</span>
          </div>
        </div>

        {/* Main Nav */}
        <span className="sidebar-section-label">Main</span>

        {[
          { key: 'dashboard', label: 'Dashboard' },
          { key: 'predict',   label: 'Predictor' },
          { key: 'analytics', label: 'Analytics' },
          { key: 'watchlist', label: 'Watchlist', badge: 'NEW' },
        ].map(({ key, label, badge }) => (
          <div
            key={key}
            className={`nav-item ${activeTab === key ? 'active' : ''}`}
            onClick={() => setActiveTab(key)}
          >
            <span className="nav-icon">
              <Icon d={ICONS[key]} />
            </span>
            {label}
            {badge && <span className="nav-badge">{badge}</span>}
          </div>
        ))}

        {/* Footer User Block */}
        <div className="sidebar-footer">
          <div className="sidebar-user">
            <div className="sidebar-avatar">HR</div>
            <div className="sidebar-user-info">
              <div className="sidebar-user-name">Admin User</div>
              <div className="sidebar-user-role">HR Analyst</div>
            </div>
          </div>
        </div>
      </aside>

      {/* ══ MAIN AREA ════════════════════════════ */}
      <div className="main-area">
        {/* Top Header */}
        <header className="top-header">
          <div className="header-title-group">
            <span className="header-title">{meta.title}</span>
            <span className="header-subtitle">{meta.subtitle}</span>
          </div>
          <div className="header-actions">
            <span className="header-badge">Models Online</span>
          </div>
        </header>

        {/* Page */}
        <main className="page-content">
          <div key={activeTab} className="animate-in">
            {activeTab === 'dashboard' && <Dashboard />}
            {activeTab === 'predict'   && <PredictForm />}
            {activeTab === 'analytics' && <Analytics />}
            {activeTab === 'watchlist' && <Watchlist />}
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
