import { useNavigate } from 'react-router-dom'
import { TrendingUp, TrendingDown, Minus, ChevronRight } from 'lucide-react'

function trendIcon(trend) {
  if (trend === 'up') return <TrendingUp size={14} className="trend-up" />
  if (trend === 'down') return <TrendingDown size={14} className="trend-down" />
  return <Minus size={14} className="trend-stable" />
}

function scoreColor(score) {
  if (score >= 80) return 'var(--score-excellent)'
  if (score >= 60) return 'var(--score-good)'
  if (score >= 40) return 'var(--score-average)'
  return 'var(--score-poor)'
}

export default function TeamTable({ employees }) {
  const navigate = useNavigate()

  if (!employees || employees.length === 0) {
    return <div className="empty-state">No scores yet. Waiting for data collection...</div>
  }

  return (
    <div className="team-table-wrap">
      <table className="team-table">
        <thead>
          <tr>
            <th>Employee</th>
            <th>Role</th>
            <th>Score</th>
            <th>Task</th>
            <th>Timeliness</th>
            <th>Comms</th>
            <th>Engagement</th>
            <th>Trend</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {employees.map(emp => (
            <tr
              key={emp.employee_id}
              className="team-row"
              onClick={() => navigate(`/employee/${emp.employee_id}`)}
            >
              <td className="team-name">{emp.employee_name}</td>
              <td className="team-role">{emp.employee_role}</td>
              <td>
                <span className="team-score" style={{ color: scoreColor(emp.current_score) }}>
                  {Math.round(emp.current_score)}
                </span>
              </td>
              <td className="team-sub">{Math.round(emp.task_score)}</td>
              <td className="team-sub">{Math.round(emp.timeliness_score)}</td>
              <td className="team-sub">{Math.round(emp.communication_score)}</td>
              <td className="team-sub">{Math.round(emp.engagement_score)}</td>
              <td>{trendIcon(emp.trend)}</td>
              <td><ChevronRight size={14} className="team-chevron" /></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
