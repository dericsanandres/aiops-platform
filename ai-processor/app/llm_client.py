import logging
from openai import OpenAI
from typing import Optional

from .config import get_settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an AIOps assistant that analyzes infrastructure alerts.
When given an alert, provide:
1. A brief summary of what's happening
2. Potential root causes (2-3 possibilities)
3. Recommended actions to resolve the issue
4. Severity assessment (Critical/Warning/Info)

Be concise and actionable. Format your response clearly."""


class LLMClient:
    """OpenAI LLM client for alert analysis."""

    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    async def analyze_alert(self, alert_data: dict) -> str:
        """Analyze an alert using OpenAI."""
        try:
            # Format alert for analysis
            alert_text = self._format_alert(alert_data)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Analyze this alert:\n\n{alert_text}"},
                ],
                max_tokens=500,
                temperature=0.3,
            )

            analysis = response.choices[0].message.content
            logger.info(f"Alert analyzed successfully")
            return analysis

        except Exception as e:
            logger.error(f"Error analyzing alert: {e}")
            return f"Error analyzing alert: {str(e)}"

    def _format_alert(self, alert_data: dict) -> str:
        """Format alert data for LLM consumption."""
        alerts = alert_data.get("alerts", [])
        if not alerts:
            return "No alert data provided"

        formatted_alerts = []
        for alert in alerts:
            labels = alert.get("labels", {})
            annotations = alert.get("annotations", {})

            formatted = f"""
Alert: {labels.get('alertname', 'Unknown')}
Severity: {labels.get('severity', 'Unknown')}
Status: {alert.get('status', 'Unknown')}
Instance: {labels.get('instance', 'Unknown')}
Job: {labels.get('job', 'Unknown')}
Summary: {annotations.get('summary', 'N/A')}
Description: {annotations.get('description', 'N/A')}
Started: {alert.get('startsAt', 'Unknown')}
"""
            formatted_alerts.append(formatted)

        return "\n---\n".join(formatted_alerts)


# Singleton instance
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get or create LLM client instance."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
