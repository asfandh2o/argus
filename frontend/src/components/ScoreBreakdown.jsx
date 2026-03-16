import { CheckCircle, Clock, MessageSquare, Zap } from 'lucide-react'

const categories = [
  { key: 'task_score', label: 'Task Completion', weight: '40%', icon: CheckCircle, color: '#22c55e' },
  { key: 'timeliness_score', label: 'Timeliness', weight: '25%', icon: Clock, color: '#06b6d4' },
  { key: 'communication_score', label: 'Communication', weight: '20%', icon: MessageSquare, color: '#8b5cf6' },
  { key: 'engagement_score', label: 'Engagement', weight: '15%', icon: Zap, color: '#f59e0b' },
]

export default function ScoreBreakdown({ score }) {
  if (!score) return null

  return (
    <div className="score-breakdown">
      {categories.map(cat => {
        const value = score[cat.key] || 0
        const Icon = cat.icon
        return (
          <div key={cat.key} className="breakdown-row">
            <div className="breakdown-label">
              <Icon size={14} style={{ color: cat.color }} />
              <span>{cat.label}</span>
              <span className="breakdown-weight">{cat.weight}</span>
            </div>
            <div className="breakdown-bar-wrap">
              <div
                className="breakdown-bar"
                style={{ width: `${value}%`, background: cat.color }}
              />
            </div>
            <span className="breakdown-value">{Math.round(value)}</span>
          </div>
        )
      })}
    </div>
  )
}
