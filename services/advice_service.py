from groq import AsyncGroq
from core.config import settings
from core.logging import get_logger
from models.advice import Advice
import json

logger = get_logger(__name__)


class AdviceService:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.LLM_MODEL

    async def generate(self, employee, score, hera_metrics: dict, echo_metrics: dict) -> list:
        """Generate 2-4 actionable advice items based on score breakdown."""
        prompt = f"""You are ARGUS, a productivity intelligence advisor.
Analyze this employee's productivity data and provide 2-4 specific, actionable recommendations.

Employee: {employee.name} ({employee.role})
Overall Score: {score.overall_score}/100

Score Breakdown:
- Task Completion: {score.task_score}/100 (weight: 40%)
- Timeliness: {score.timeliness_score}/100 (weight: 25%)
- Communication: {score.communication_score}/100 (weight: 20%)
- Engagement: {score.engagement_score}/100 (weight: 15%)

Task Data (from HERA):
- Tasks completed: {hera_metrics.get('tasks_completed', 0)}/{hera_metrics.get('tasks_total', 0)}
- On-time: {hera_metrics.get('on_time_completions', 0)}/{hera_metrics.get('tasks_with_deadline', 0)}

Activity Data (from ECHO):
- Emails received: {echo_metrics.get('emails_received', 0)}
- Suggestions accepted: {echo_metrics.get('suggestions_accepted', 0)}/{echo_metrics.get('suggestions_total', 0)}
- Notifications read: {echo_metrics.get('notifications_read', 0)}/{echo_metrics.get('notifications_total', 0)}
- Meeting hours: {echo_metrics.get('meeting_hours', 0)}

Return a JSON array where each item has:
- "content": The advice text (1-2 sentences, specific and actionable)
- "category": One of "focus", "time_management", "communication", "engagement"
- "priority": "high" if that area's score < 50, "medium" if 50-75, "low" if > 75

Focus on the weakest areas. Be specific, not generic.
Return ONLY valid JSON array. No markdown, no explanation."""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a productivity advisor. Return only valid JSON."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
                max_tokens=1000,
            )

            raw = response.choices[0].message.content.strip()
            # Strip markdown code blocks if present
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
                if raw.endswith("```"):
                    raw = raw[:-3]
                raw = raw.strip()

            items = json.loads(raw)
            advice_list = []
            for item in items:
                advice_list.append(Advice(
                    employee_id=employee.id,
                    score_id=score.id,
                    content=item["content"],
                    category=item.get("category", "focus"),
                    priority=item.get("priority", "medium"),
                    context={
                        "overall_score": score.overall_score,
                        "task_score": score.task_score,
                        "timeliness_score": score.timeliness_score,
                        "communication_score": score.communication_score,
                        "engagement_score": score.engagement_score,
                    },
                ))

            logger.info("advice_generated", employee=employee.email, count=len(advice_list))
            return advice_list

        except json.JSONDecodeError as e:
            logger.error("advice_json_parse_error", error=str(e))
            return []
        except Exception as e:
            error_msg = str(e).lower()
            if "rate_limit" in error_msg or "429" in error_msg:
                logger.warning("advice_rate_limited", error=str(e))
            else:
                logger.error("advice_generation_error", error=str(e))
            return []
