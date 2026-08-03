import React, { useState } from 'react';

const Login = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    // Simulate network latency for authenticity
    await new Promise(r => setTimeout(r, 600));
    if (email.includes('@') && password.length >= 4) {
      onLogin(true);
    } else {
      setError('Invalid credentials. Please check your email and password.');
    }
    setLoading(false);
  };

  return (
    <div className="login-shell">
      {/* ── Left Visual Panel ── */}
      <div className="login-visual">
        <div className="login-visual-content">
          <div className="login-brand">
            <div className="login-brand-icon">📊</div>
            <span className="login-brand-name">PeopleIQ Analytics</span>
          </div>

          <div className="login-hero-text">
            <h1>
              <span className="gradient-text">Predict</span> attrition<br />
              before it happens.
            </h1>
            <p>
              Harness machine learning to identify at-risk employees, 
              uncover retention drivers, and make data-informed HR decisions.
            </p>
          </div>

          <div className="login-stats">
            <div className="login-stat">
              <span className="login-stat-value">84%</span>
              <span className="login-stat-label">Model Accuracy</span>
            </div>
            <div className="login-stat">
              <span className="login-stat-value">1,470</span>
              <span className="login-stat-label">Employees Tracked</span>
            </div>
            <div className="login-stat">
              <span className="login-stat-value">3</span>
              <span className="login-stat-label">ML Models Active</span>
            </div>
          </div>
        </div>

        <div className="login-testimonial">
          <p className="login-testimonial-text">
            "This platform helped us reduce voluntary attrition by 34% in just two quarters. 
            The risk predictions are incredibly accurate."
          </p>
          <div className="login-testimonial-author">
            <div className="login-testimonial-avatar">SR</div>
            <div>
              <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-1)' }}>Sarah R.</div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-3)' }}>VP of People Operations</div>
            </div>
          </div>
        </div>
      </div>

      {/* ── Right Form Panel ── */}
      <div className="login-form-panel">
        <div className="login-form-box animate-in">
          <h2>Welcome back</h2>
          <p className="text-muted mb-6" style={{ marginTop: '0.4rem', fontSize: '0.875rem' }}>
            Sign in to your HR Analytics dashboard
          </p>

          <div className="login-hint">
            <strong>Demo:</strong> Use any email &amp; password with 4+ characters
          </div>

          {error && (
            <div style={{
              background: 'var(--danger-bg)',
              border: '1px solid var(--danger-border)',
              color: 'var(--danger)',
              borderRadius: 'var(--r-md)',
              padding: '0.75rem 1rem',
              fontSize: '0.825rem',
              marginBottom: '1rem'
            }}>
              ⚠️ {error}
            </div>
          )}

          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div className="form-group">
              <label>Email address</label>
              <div className="input-group">
                <span className="input-group-icon" style={{ fontSize: '0.875rem' }}>✉️</span>
                <input
                  type="email"
                  className="form-control"
                  placeholder="hr@company.com"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <div className="flex justify-between items-center">
                <label>Password</label>
                <span style={{ fontSize: '0.75rem', color: 'var(--brand-blue)', cursor: 'pointer' }}>
                  Forgot password?
                </span>
              </div>
              <div className="input-group">
                <span className="input-group-icon" style={{ fontSize: '0.875rem' }}>🔒</span>
                <input
                  type="password"
                  className="form-control"
                  placeholder="••••••••"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-block btn-lg"
              disabled={loading}
              style={{ marginTop: '0.5rem' }}
            >
              {loading ? (
                <>
                  <div className="spinner" style={{ width: 16, height: 16 }} />
                  Signing in...
                </>
              ) : (
                'Sign In →'
              )}
            </button>
          </form>

          <p style={{ marginTop: '1.5rem', fontSize: '0.75rem', color: 'var(--text-3)', textAlign: 'center' }}>
            By signing in, you agree to the{' '}
            <span style={{ color: 'var(--brand-blue)', cursor: 'pointer' }}>Terms of Service</span>
            {' '}and{' '}
            <span style={{ color: 'var(--brand-blue)', cursor: 'pointer' }}>Privacy Policy</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
