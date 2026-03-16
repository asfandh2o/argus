from datetime import date
from models.productivity_score import ProductivityScore


class ScoringEngine:
    """Transparent, math-based productivity scoring.

    All weights and factors are stored in each score record
    so employees can see exactly how their score was calculated.
    """

    WEIGHTS = {
        "task": 0.40,
        "timeliness": 0.25,
        "communication": 0.20,
        "engagement": 0.15,
    }

    def calculate(
        self,
        employee_id,
        hera_metrics: dict,
        echo_metrics: dict,
        score_date: date,
    ) -> ProductivityScore:
        task_score = self._calc_task_score(hera_metrics)
        timeliness_score = self._calc_timeliness_score(hera_metrics)
        communication_score = self._calc_communication_score(echo_metrics)
        engagement_score = self._calc_engagement_score(echo_metrics)

        overall = (
            task_score * self.WEIGHTS["task"]
            + timeliness_score * self.WEIGHTS["timeliness"]
            + communication_score * self.WEIGHTS["communication"]
            + engagement_score * self.WEIGHTS["engagement"]
        )

        raw_metrics = {
            "tasks_total": hera_metrics.get("tasks_total", 0),
            "tasks_completed": hera_metrics.get("tasks_completed", 0),
            "on_time_completions": hera_metrics.get("on_time_completions", 0),
            "tasks_with_deadline": hera_metrics.get("tasks_with_deadline", 0),
            "priority_weighted_completed": hera_metrics.get("priority_weighted_completed", 0),
            "emails_received": echo_metrics.get("emails_received", 0),
            "suggestions_total": echo_metrics.get("suggestions_total", 0),
            "suggestions_accepted": echo_metrics.get("suggestions_accepted", 0),
            "suggestions_rejected": echo_metrics.get("suggestions_rejected", 0),
            "suggestions_edited": echo_metrics.get("suggestions_edited", 0),
            "calendar_events": echo_metrics.get("calendar_events", 0),
            "meeting_hours": echo_metrics.get("meeting_hours", 0),
            "notifications_total": echo_metrics.get("notifications_total", 0),
            "notifications_read": echo_metrics.get("notifications_read", 0),
            "notifications_actioned": echo_metrics.get("notifications_actioned", 0),
        }

        return ProductivityScore(
            employee_id=employee_id,
            score_date=score_date,
            overall_score=round(overall, 1),
            task_score=round(task_score, 1),
            timeliness_score=round(timeliness_score, 1),
            communication_score=round(communication_score, 1),
            engagement_score=round(engagement_score, 1),
            weights=self.WEIGHTS,
            raw_metrics=raw_metrics,
        )

    def _calc_task_score(self, hera: dict) -> float:
        """0-100 based on completion rate and priority-weighted output."""
        total = hera.get("tasks_total", 0)
        completed = hera.get("tasks_completed", 0)
        if total == 0:
            return 50.0  # Neutral if no tasks assigned

        completion_rate = completed / total
        pw = hera.get("priority_weighted_completed", completed)
        priority_ratio = pw / max(completed, 1)

        score = completion_rate * 80 + min(priority_ratio / 2.0, 1.0) * 20
        return min(score, 100.0)

    def _calc_timeliness_score(self, hera: dict) -> float:
        """0-100 based on on-time delivery rate."""
        with_deadline = hera.get("tasks_with_deadline", 0)
        on_time = hera.get("on_time_completions", 0)
        if with_deadline == 0:
            return 75.0  # Neutral-positive if no deadlines set

        return (on_time / with_deadline) * 100.0

    def _calc_communication_score(self, echo: dict) -> float:
        """0-100 based on email suggestion engagement."""
        suggestions_total = echo.get("suggestions_total", 0)
        accepted = echo.get("suggestions_accepted", 0)
        edited = echo.get("suggestions_edited", 0)
        if suggestions_total == 0:
            return 60.0  # Neutral if no suggestions generated

        engagement_rate = (accepted + edited) / suggestions_total
        return min(engagement_rate * 100.0, 100.0)

    def _calc_engagement_score(self, echo: dict) -> float:
        """0-100 based on notification read/action rate."""
        notif_total = echo.get("notifications_total", 0)
        notif_read = echo.get("notifications_read", 0)
        notif_actioned = echo.get("notifications_actioned", 0)
        if notif_total == 0:
            return 50.0  # Neutral if no notifications

        read_rate = notif_read / notif_total
        action_rate = notif_actioned / notif_total
        return min((read_rate * 0.7 + action_rate * 0.3) * 100.0, 100.0)
