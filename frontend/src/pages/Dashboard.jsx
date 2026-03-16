import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { api } from '../api'
import { Eye, LogOut, Users, TrendingUp, Award, AlertTriangle, BarChart3 } from 'lucide-react'
import ScoreGauge from '../components/ScoreGauge'
import TeamTable from '../components/TeamTable'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [teamSummary, setTeamSummary] = useState([])
  const [loading, setLoading] = useState(true)
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    const load = async () => {
      try {
        const [s, t] = await Promise.all([
          api.teamStats(),
          api.teamSummary(),
        ])
        setStats(s)
        setTeamSummary(t)
      } catch (err) {
        console.error('Failed to load dashboard:', err)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="header-left">
          <Eye size={20} className="header-logo" />
          <h1 className="header-title">ARGUS</h1>
          <span className="header-subtitle">Productivity Intelligence</span>
        </div>
        <div className="header-right">
          <span className="header-user">{user?.name || user?.email}</span>
          <button className="btn-icon" onClick={handleLogout} title="Logout">
            <LogOut size={16} />
          </button>
        </div>
      </header>

      <main className="app-content">
        {loading ? (
          <div className="loading-state">Loading dashboard...</div>
        ) : (
          <>
            {/* Stats cards */}
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon"><Users size={20} /></div>
                <div className="stat-info">
                  <span className="stat-value">{stats?.employee_count || 0}</span>
                  <span className="stat-label">Employees</span>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon accent"><BarChart3 size={20} /></div>
                <div className="stat-info">
                  <span className="stat-value">{stats?.team_average || 0}</span>
                  <span className="stat-label">Team Average</span>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon success"><Award size={20} /></div>
                <div className="stat-info">
                  <span className="stat-value">{stats?.highest_scorer?.name || '—'}</span>
                  <span className="stat-label">Top Performer ({stats?.highest_scorer?.score || 0})</span>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon warning"><AlertTriangle size={20} /></div>
                <div className="stat-info">
                  <span className="stat-value">{stats?.lowest_scorer?.name || '—'}</span>
                  <span className="stat-label">Needs Support ({stats?.lowest_scorer?.score || 0})</span>
                </div>
              </div>
            </div>

            {/* Category averages */}
            {stats?.category_averages && Object.keys(stats.category_averages).length > 0 && (
              <div className="card section-card">
                <h2 className="section-title">Category Averages</h2>
                <div className="category-bars">
                  {Object.entries(stats.category_averages).map(([key, value]) => (
                    <div key={key} className="category-bar-row">
                      <span className="category-label">{key.charAt(0).toUpperCase() + key.slice(1)}</span>
                      <div className="category-bar-track">
                        <div className="category-bar-fill" style={{ width: `${value}%` }} />
                      </div>
                      <span className="category-value">{value}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Team leaderboard */}
            <div className="card section-card">
              <h2 className="section-title">
                <TrendingUp size={16} /> Team Scores
              </h2>
              <TeamTable employees={teamSummary} />
            </div>
          </>
        )}
      </main>
    </div>
  )
}
