import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../api'
import { ArrowLeft, Eye, ChevronDown, ChevronUp } from 'lucide-react'
import ScoreGauge from '../components/ScoreGauge'
import ScoreBreakdown from '../components/ScoreBreakdown'
import AdviceCard from '../components/AdviceCard'

export default function EmployeeDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [scores, setScores] = useState([])
  const [advice, setAdvice] = useState([])
  const [loading, setLoading] = useState(true)
  const [showRaw, setShowRaw] = useState(false)

  useEffect(() => {
    const load = async () => {
      try {
        const [s, a] = await Promise.all([
          api.employeeScores(id),
          api.employeeAdvice(id),
        ])
        setScores(s)
        setAdvice(a)
      } catch (err) {
        console.error('Failed to load employee:', err)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [id])

  const latest = scores[0] || null

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="header-left">
          <button className="btn-icon" onClick={() => navigate('/dashboard')}>
            <ArrowLeft size={18} />
          </button>
          <Eye size={20} className="header-logo" />
          <h1 className="header-title">Employee Detail</h1>
        </div>
      </header>

      <main className="app-content">
        {loading ? (
          <div className="loading-state">Loading...</div>
        ) : !latest ? (
          <div className="empty-state">No scores available for this employee yet.</div>
        ) : (
          <>
            {/* Score gauge + breakdown */}
            <div className="detail-top">
              <div className="card detail-gauge-card">
                <ScoreGauge score={latest.overall_score} size={180} />
                <div className="detail-date">
                  Score for {new Date(latest.score_date).toLocaleDateString()}
                </div>
              </div>
              <div className="card detail-breakdown-card">
                <h3>Score Breakdown</h3>
                <ScoreBreakdown score={latest} />
              </div>
            </div>

            {/* AI Advice */}
            {advice.length > 0 && (
              <div className="card section-card">
                <h2 className="section-title">AI Recommendations</h2>
                <div className="advice-list">
                  {advice.map(a => (
                    <AdviceCard key={a.id} advice={a} />
                  ))}
                </div>
              </div>
            )}

            {/* Raw metrics */}
            <div className="card section-card">
              <button className="raw-toggle" onClick={() => setShowRaw(!showRaw)}>
                <span>Raw Metrics</span>
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
