import { X, Lightbulb, Clock, MessageSquare, Zap, Target } from 'lucide-react'

const categoryIcons = {
  focus: Target,
  time_management: Clock,
  communication: MessageSquare,
  engagement: Zap,
}

const priorityColors = {
  high: '#ef4444',
  medium: '#f59e0b',
  low: '#22c55e',
}

export default function AdviceCard({ advice, onDismiss }) {
  const Icon = categoryIcons[advice.category] || Lightbulb
  const pColor = priorityColors[advice.priority] || '#f59e0b'

  return (
    <div className="advice-card">
      <div className="advice-icon" style={{ color: pColor }}>
        <Icon size={16} />
      </div>
      <div className="advice-content">
        <div className="advice-text">{advice.content}</div>
        <div className="advice-meta">
          <span className="advice-category">{advice.category.replace('_', ' ')}</span>
          <span className="advice-priority" style={{ color: pColor }}>
            {advice.priority}
          </span>
        </div>
      </div>
      {onDismiss && (
        <button className="advice-dismiss" onClick={() => onDismiss(advice.id)} title="Dismiss">
          <X size={14} />
        </button>
      )}
    </div>
  )
}
