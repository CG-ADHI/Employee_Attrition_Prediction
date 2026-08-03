import React, { useState, useMemo } from 'react';

/* ── Sample watchlist data (representative of at-risk profile) ── */
const AT_RISK_DATA = [
  { id: 1,  name: 'Alex Carter',     dept: 'Sales',   role: 'Sales Representative',  income: 2500, tenure: 1, overtime: 'Yes', satisfaction: 1, risk: 0.91, level: 'HIGH' },
  { id: 2,  name: 'Maria Fernández', dept: 'Sales',   role: 'Sales Executive',        income: 3100, tenure: 2, overtime: 'Yes', satisfaction: 2, risk: 0.84, level: 'HIGH' },
  { id: 3,  name: 'David Kim',       dept: 'R&D',     role: 'Laboratory Technician', income: 2800, tenure: 1, overtime: 'Yes', satisfaction: 1, risk: 0.79, level: 'HIGH' },
  { id: 4,  name: 'Priya Sharma',    dept: 'HR',      role: 'Human Resources',       income: 2200, tenure: 3, overtime: 'No',  satisfaction: 2, risk: 0.74, level: 'HIGH' },
  { id: 5,  name: 'Tom Willis',      dept: 'Sales',   role: 'Sales Representative',  income: 2700, tenure: 2, overtime: 'Yes', satisfaction: 2, risk: 0.71, level: 'HIGH' },
  { id: 6,  name: 'Nadia Okonkwo',   dept: 'R&D',     role: 'Research Scientist',    income: 4200, tenure: 4, overtime: 'Yes', satisfaction: 2, risk: 0.65, level: 'HIGH' },
  { id: 7,  name: 'James Patel',     dept: 'Sales',   role: 'Sales Executive',        income: 3800, tenure: 5, overtime: 'Yes', satisfaction: 3, risk: 0.61, level: 'HIGH' },
  { id: 8,  name: 'Sophie Laurent',  dept: 'HR',      role: 'Human Resources',       income: 2600, tenure: 2, overtime: 'No',  satisfaction: 2, risk: 0.58, level: 'MEDIUM' },
  { id: 9,  name: 'Ravi Mehta',      dept: 'R&D',     role: 'Laboratory Technician', income: 3100, tenure: 6, overtime: 'No',  satisfaction: 2, risk: 0.54, level: 'MEDIUM' },
  { id: 10, name: 'Claire Dubois',   dept: 'Sales',   role: 'Sales Representative',  income: 2900, tenure: 3, overtime: 'Yes', satisfaction: 3, risk: 0.52, level: 'MEDIUM' },
  { id: 11, name: 'Marcus Johnson',  dept: 'R&D',     role: 'Research Scientist',    income: 5500, tenure: 7, overtime: 'No',  satisfaction: 3, risk: 0.45, level: 'MEDIUM' },
  { id: 12, name: 'Aisha Bello',     dept: 'HR',      role: 'Human Resources',       income: 3000, tenure: 4, overtime: 'No',  satisfaction: 3, risk: 0.41, level: 'MEDIUM' },
  { id: 13, name: 'Luke Patterson',  dept: 'Sales',   role: 'Sales Executive',        income: 4500, tenure: 8, overtime: 'No',  satisfaction: 3, risk: 0.38, level: 'MEDIUM' },
  { id: 14, name: 'Emma Nguyen',     dept: 'R&D',     role: 'Manager',               income: 9200, tenure: 12, overtime: 'No', satisfaction: 4, risk: 0.22, level: 'LOW' },
  { id: 15, name: 'Carlos Reyes',    dept: 'R&D',     role: 'Research Director',     income: 13500, tenure: 15, overtime: 'No',satisfaction: 4, risk: 0.18, level: 'LOW' },
];

const LEVEL_CONFIG = {
  HIGH:   { label: 'HIGH',   cls: 'badge-red',   dot: 'var(--danger)',  sortVal: 3 },
  MEDIUM: { label: 'MEDIUM', cls: 'badge-amber',  dot: 'var(--warning)', sortVal: 2 },
  LOW:    { label: 'LOW',    cls: 'badge-green',  dot: 'var(--success)', sortVal: 1 },
};

const DEPT_OPTIONS = ['All', 'Sales', 'R&D', 'HR'];

const Watchlist = () => {
  const [search, setSearch]   = useState('');
  const [dept, setDept]       = useState('All');
  const [filter, setFilter]   = useState('All'); // All, HIGH, MEDIUM, LOW
  const [sortKey, setSortKey] = useState('risk');
  const [sortDir, setSortDir] = useState('desc');
  const [selected, setSelected] = useState(null);

  const handleSort = key => {
    if (sortKey === key) setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    else { setSortKey(key); setSortDir('desc'); }
  };

  const rows = useMemo(() => {
    return AT_RISK_DATA
      .filter(e =>
        (dept === 'All' || e.dept === dept) &&
        (filter === 'All' || e.level === filter) &&
        (search === '' || e.name.toLowerCase().includes(search.toLowerCase()) || e.role.toLowerCase().includes(search.toLowerCase()))
      )
      .sort((a, b) => {
        let av = a[sortKey], bv = b[sortKey];
        if (sortKey === 'level') { av = LEVEL_CONFIG[a.level].sortVal; bv = LEVEL_CONFIG[b.level].sortVal; }
        return sortDir === 'desc' ? (bv > av ? 1 : -1) : (av > bv ? 1 : -1);
      });
  }, [search, dept, filter, sortKey, sortDir]);

  const summary = {
    high:   AT_RISK_DATA.filter(e => e.level === 'HIGH').length,
    medium: AT_RISK_DATA.filter(e => e.level === 'MEDIUM').length,
    low:    AT_RISK_DATA.filter(e => e.level === 'LOW').length,
  };

  const SortIcon = ({ k }) => (
    <span style={{ marginLeft: 4, opacity: sortKey === k ? 1 : 0.3, fontSize: '0.7rem' }}>
      {sortKey === k ? (sortDir === 'desc' ? '▼' : '▲') : '⇅'}
    </span>
  );

  return (
    <div>
      {/* Summary Cards */}
      <div className="grid grid-3 mb-6 stagger">
        {[
          { level: 'HIGH',   count: summary.high,   icon: '🔴', color: 'var(--danger)',  sub: 'Probability > 60%' },
          { level: 'MEDIUM', count: summary.medium, icon: '🟡', color: 'var(--warning)', sub: 'Probability 30–60%' },
          { level: 'LOW',    count: summary.low,    icon: '🟢', color: 'var(--success)', sub: 'Probability < 30%' },
        ].map(c => (
          <div key={c.level} className="card" style={{ cursor: 'pointer', borderLeft: `3px solid ${c.color}`, transition: 'all 0.2s' }}
            onClick={() => setFilter(f => f === c.level ? 'All' : c.level)}>
            <div className="flex items-center justify-between mb-2">
              <span style={{ fontSize: '1.4rem' }}>{c.icon}</span>
              <span className={`badge ${LEVEL_CONFIG[c.level].cls}`}>{filter === c.level ? 'Filtered ✓' : c.level}</span>
            </div>
            <div className="card-value">{c.count}</div>
            <div className="card-sub">{c.sub}</div>
          </div>
        ))}
      </div>

      {/* Table Card */}
      <div className="card p-0">
        {/* Toolbar */}
        <div className="flex items-center gap-3 p-4" style={{ borderBottom: '1px solid var(--border-1)' }}>
          <div className="input-group" style={{ flex: 1, maxWidth: 280 }}>
            <span className="input-group-icon">🔍</span>
            <input className="form-control" placeholder="Search by name or role…"
              value={search} onChange={e => setSearch(e.target.value)} />
          </div>
          <select className="form-control" style={{ width: 'auto', minWidth: 130 }}
            value={dept} onChange={e => setDept(e.target.value)}>
            {DEPT_OPTIONS.map(d => <option key={d}>{d}</option>)}
          </select>
          {filter !== 'All' && (
            <button className="btn btn-ghost btn-sm" onClick={() => setFilter('All')}>
              Clear filter ✕
            </button>
          )}
          <span className="text-muted text-sm" style={{ marginLeft: 'auto' }}>
            {rows.length} / {AT_RISK_DATA.length} employees
          </span>
        </div>

        {/* Table */}
        <div className="data-table-wrapper" style={{ borderRadius: 0, border: 'none' }}>
          <table className="data-table">
            <thead>
              <tr>
                {[
                  { label: 'Employee',     key: 'name' },
                  { label: 'Department',   key: 'dept' },
                  { label: 'Role',         key: 'role' },
                  { label: 'Income',       key: 'income' },
                  { label: 'Tenure (yrs)', key: 'tenure' },
                  { label: 'Overtime',     key: 'overtime' },
                  { label: 'Satisfaction', key: 'satisfaction' },
                  { label: 'Risk %',       key: 'risk' },
                  { label: 'Level',        key: 'level' },
                ].map(col => (
                  <th key={col.key} onClick={() => handleSort(col.key)}>
                    {col.label} <SortIcon k={col.key} />
                  </th>
                ))}
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {rows.map(emp => {
                const lc = LEVEL_CONFIG[emp.level];
                const isSelected = selected === emp.id;
                return (
                  <tr key={emp.id}
                    style={isSelected ? { background: 'rgba(79,142,247,0.08)' } : {}}
                    onClick={() => setSelected(isSelected ? null : emp.id)}>
                    <td>
                      <div className="flex items-center gap-2">
                        <div style={{
                          width: 28, height: 28, borderRadius: '50%', flexShrink: 0,
                          background: `linear-gradient(135deg, ${lc.dot}40, ${lc.dot}20)`,
                          border: `1px solid ${lc.dot}50`,
                          display: 'flex', alignItems: 'center', justifyContent: 'center',
                          fontSize: '0.65rem', fontWeight: 700, color: lc.dot,
                        }}>
                          {emp.name.split(' ').map(n => n[0]).join('')}
                        </div>
                        {emp.name}
                      </div>
                    </td>
                    <td>
                      <span className={`badge ${emp.dept === 'Sales' ? 'badge-amber' : emp.dept === 'R&D' ? 'badge-blue' : 'badge-purple'}`}>
                        {emp.dept}
                      </span>
                    </td>
                    <td style={{ color: 'var(--text-2)' }}>{emp.role}</td>
                    <td>₹{emp.income.toLocaleString()}</td>
                    <td>{emp.tenure} yrs</td>
                    <td>
                      <span className={`badge ${emp.overtime === 'Yes' ? 'badge-red' : 'badge-green'}`}>
                        {emp.overtime}
                      </span>
                    </td>
                    <td>
                      <div className="flex items-center gap-2">
                        {[1,2,3,4].map(n => (
                          <div key={n} style={{
                            width: 6, height: 6, borderRadius: '50%',
                            background: n <= emp.satisfaction ? 'var(--brand-blue)' : 'var(--surface-5)',
                          }} />
                        ))}
                      </div>
                    </td>
                    <td>
                      <div className="flex items-center gap-2">
                        <div className="progress-bar" style={{ width: 60 }}>
                          <div className="progress-fill" style={{
                            width: `${emp.risk * 100}%`,
                            background: emp.level === 'HIGH' ? 'var(--danger)' : emp.level === 'MEDIUM' ? 'var(--warning)' : 'var(--success)'
                          }} />
                        </div>
                        <span style={{ fontWeight: 700, fontSize: '0.82rem',
                          color: emp.level === 'HIGH' ? 'var(--danger)' : emp.level === 'MEDIUM' ? 'var(--warning)' : 'var(--success)' }}>
                          {(emp.risk * 100).toFixed(0)}%
                        </span>
                      </div>
                    </td>
                    <td><span className={`badge ${lc.cls}`}>{lc.label}</span></td>
                    <td onClick={e => e.stopPropagation()}>
                      <div className="flex gap-1">
                        <button className="btn btn-ghost btn-sm" title="Schedule Review">📅</button>
                        <button className="btn btn-ghost btn-sm" title="View Profile">👤</button>
                      </div>
                    </td>
                  </tr>
                );
              })}
              {rows.length === 0 && (
                <tr>
                  <td colSpan={10}>
                    <div className="empty-state">
                      <div className="empty-icon">🔍</div>
                      <p className="text-muted text-sm">No employees match your filters.</p>
                    </div>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-4" style={{ borderTop: '1px solid var(--border-1)' }}>
          <span className="text-muted text-sm">
            💡 Click a row to highlight · Click column headers to sort
          </span>
          <button className="btn btn-secondary btn-sm" onClick={() => {
            const csv = ['Name,Department,Role,Income,Tenure,OverTime,Satisfaction,Risk%,Level',
              ...rows.map(e => `${e.name},${e.dept},${e.role},${e.income},${e.tenure},${e.overtime},${e.satisfaction},${(e.risk*100).toFixed(0)},${e.level}`)
            ].join('\n');
            const a = document.createElement('a');
            a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
            a.download = 'at_risk_watchlist.csv';
            a.click();
          }}>
            ⬇ Export CSV
          </button>
        </div>
      </div>
    </div>
  );
};

export default Watchlist;
