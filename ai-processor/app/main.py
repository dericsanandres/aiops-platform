import logging
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from .config import get_settings
from .llm_client import get_llm_client

# Configure logging
settings = get_settings()
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Prometheus metrics
ALERTS_RECEIVED = Counter(
    "aiops_alerts_received_total", "Total number of alerts received", ["severity"]
)
ALERTS_ANALYZED = Counter(
    "aiops_alerts_analyzed_total", "Total number of alerts analyzed", ["status"]
)
ANALYSIS_DURATION = Histogram(
    "aiops_analysis_duration_seconds", "Time spent analyzing alerts"
)

# FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered alert analysis for AIOps",
    version="1.0.0",
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": settings.app_name,
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/webhook/alertmanager")
async def alertmanager_webhook(request: Request):
    """
    Webhook endpoint for Alertmanager.
    Receives alerts and analyzes them using OpenAI.
    """
    try:
        alert_data = await request.json()
        logger.info(f"Received alert webhook: {alert_data.get('status', 'unknown')}")

        # Count alerts by severity
        alerts = alert_data.get("alerts", [])
        for alert in alerts:
            severity = alert.get("labels", {}).get("severity", "unknown")
            ALERTS_RECEIVED.labels(severity=severity).inc()

        # Check if we have an API key
        if not settings.openai_api_key:
            logger.warning("No OpenAI API key configured - skipping analysis")
            return JSONResponse(
                content={
                    "status": "received",
                    "message": "Alert received but analysis skipped (no API key)",
                    "alert_count": len(alerts),
                },
                status_code=200,
            )

        # Analyze alert with LLM
        with ANALYSIS_DURATION.time():
            llm_client = get_llm_client()
            analysis = await llm_client.analyze_alert(alert_data)

        ALERTS_ANALYZED.labels(status="success").inc()

        # Log the analysis
        logger.info(f"Alert Analysis:\n{analysis}")

        return JSONResponse(
            content={
                "status": "analyzed",
                "alert_count": len(alerts),
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
            },
            status_code=200,
        )

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        ALERTS_ANALYZED.labels(status="error").inc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze")
async def analyze_manual(request: Request):
    """
    Manual analysis endpoint.
    Send any text for analysis.
    """
    try:
        data = await request.json()
        text = data.get("text", "")

        if not text:
            raise HTTPException(status_code=400, detail="No text provided")

        if not settings.openai_api_key:
            raise HTTPException(status_code=503, detail="No OpenAI API key configured")

        llm_client = get_llm_client()
        analysis = await llm_client.analyze_alert({"alerts": [{"annotations": {"description": text}}]})

        return JSONResponse(
            content={
                "status": "analyzed",
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
            },
            status_code=200,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in manual analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
