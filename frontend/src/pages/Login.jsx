import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { api } from '../api'
import { Eye, ShieldCheck } from 'lucide-react'

export default function Login() {
  const [mode, setMode] = useState('admin')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      let res
      if (mode === 'admin') {
        res = await api.adminLogin(email, password)
      } else {
        res = await api.employeeLogin(email)
      }
      login({ email: res.email, role: res.role, name: res.name }, res.token)
      navigate(res.role === 'admin' ? '/dashboard' : '/my-score')
    } catch (err) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-logo">
          <Eye size={32} />
          <h1>ARGUS</h1>
          <p className="login-subtitle">Productivity Intelligence</p>
        </div>

        <div className="login-tabs">
          <button
            className={`login-tab ${mode === 'admin' ? 'active' : ''}`}
            onClick={() => setMode('admin')}
          >
            <ShieldCheck size={14} /> Manager
          </button>
          <button
            className={`login-tab ${mode === 'employee' ? 'active' : ''}`}
            onClick={() => setMode('employee')}
          >
            <Eye size={14} /> Employee
          </button>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder={mode === 'admin' ? 'admin@nora.ai' : 'your@email.com'}
              required
              className="input"
            />
          </div>

          {mode === 'admin' && (
            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
                required
                className="input"
              />
            </div>
          )}

          {error && <div className="login-error">{error}</div>}

          <button type="submit" className="btn btn-primary login-btn" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
      </div>
    </div>
  )
}
