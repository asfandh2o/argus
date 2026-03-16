import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { api } from '../api'
import { Eye, LogOut, ChevronDown, ChevronUp, Info } from 'lucide-react'
import ScoreGauge from '../components/ScoreGauge'
import ScoreBreakdown from '../components/ScoreBreakdown'
import AdviceCard from '../components/AdviceCard'

export default function MyScore() {
  const [scores, setScores] = useState([])
  const [advice, setAdvice] = useState([])
  const [loading, setLoading] = useState(true)
  const [showFormula, setShowFormula] = useState(false)
  const [showRaw, setShowRaw] = useState(false)
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    const load = async () => {
      try {
        const [s, a] = await Promise.all([
          api.myScores(),
          api.myAdvice(),
        ])
        setScores(s)
        setAdvice(a)
      } catch (err) {
        console.error('Failed to load scores:', err)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const latest = scores[0] || null

  const handleDismiss = async (adviceId) => {
    try {
      await api.dismissAdvice(adviceId)
      setAdvice(prev => prev.filter(a => a.id !== adviceId))
    } catch (err) {
      console.error('Dismiss failed:', err)
    }
  }

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
          <span className="header-subtitle">My Productivity</span>
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
          <div className="loading-state">Loading your scores...</div>
        ) : !latest ? (
          <div className="empty-state">
            <Eye size={40} />
            <p style={{ marginTop: 12 }}>No scores yet</p>
            <p style={{ fontSize: 12 }}>Scores are calculated periodically from your HERA tasks and ECHO activity.</p>
          </div>
        ) : (
          <>
            {/* Score gauge + breakdown */}
            <div className="detail-top">
              <div className="card detail-gauge-card">
                <ScoreGauge score={latest.overall_score} size={180} />
                <div className="detail-date">
                  {new Date(latest.score_date).toLocaleDateString()}
                </div>
              </div>
              <div className="card detail-breakdown-card">
                <h3>Your Score Breakdown</h3>
                <ScoreBreakdown score={latest} />
              </div>
            </div>

            {/* How is my score calculated? */}
            <div className="card section-card">
              <button className="raw-toggle" onClick={() => setShowFormula(!showFormula)}>
                <span><Info size={14} /> How is my score calculated?</span>
                {showFormula ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
              </button>
              {showFormula && (
                <div className="formula-section">
                  <p>Your productivity score is a weighted composite of four transparent metrics:</p>
                  <div className="formula-block">
                    <code>
                      overall = task_score x 0.40 + timeliness_score x 0.25 + communication_score x 0.20 + engagement_score x 0.15
                    </code>
                  </div>
                  <ul className="formula-list">
                    <li><strong>Task Completion (40%)</strong> — Completion rate + priority-weighted output from HERA tasks</li>
                    <li><strong>Timeliness (25%)</strong> — On-time delivery rate for tasks with deadlines</li>
                    <li><strong>Communication (20%)</strong> — Email suggestion acceptance rate in ECHO</li>
                    <li><strong>Engagement (15%)</strong> — Notification read/action rate in ECHO</li>
                  </ul>
                  <p className="formula-note">All data is sourced transparently. No subjective factors.</p>
                </div>
              )}
            </div>

            {/* AI Advice */}
            {advice.length > 0 && (
              <div className="card section-card">
                <h2 className="section-title">Recommendations for You</h2>
                <div className="advice-list">
                  {advice.map(a => (
                    <AdviceCard key={a.id} advice={a} onDismiss={handleDismiss} />
                  ))}
                </div>
              </div>
            )}

            {/* Raw metrics */}
            <div className="card section-card">
              <button className="raw-toggle" onClick={() => setShowRaw(!showRaw)}>
                <span>Raw Data Used</span>
                {showRaw ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
              </button>
              {showRaw && (
                <div className="raw-metrics">
                  <pre>{JSON.stringify(latest.raw_metrics, null, 2)}</pre>
                </div>
              )}
            </div>

            {/* Score history */}
            {scores.length > 1 && (
              <div className="card section-card">
                <h2 className="section-title">Score History</h2>
                <div className="history-table-wrap">
                  <table className="history-table">
                    <thead>
                      <tr>
                        <th>Date</th>
                        <th>Overall</th>
                        <th>Task</th>
                        <th>Timeliness</th>
                        <th>Comms</th>
                        <th>Engagement</th>
                      </tr>
                    </thead>
                    <tbody>
                      {scores.map(s => (
                        <tr key={s.id}>
                          <td>{new Date(s.score_date).toLocaleDateString()}</td>
                          <td className="score-cell">{Math.round(s.overall_score)}</td>
                          <td>{Math.round(s.task_score)}</td>
                          <td>{Math.round(s.timeliness_score)}</td>
                          <td>{Math.round(s.communication_score)}</td>
                          <td>{Math.round(s.engagement_score)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
}
