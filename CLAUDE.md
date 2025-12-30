# AIOps Platform - Claude Code Context

> Project-specific instructions for Claude Code sessions

## Project Overview

AIOps demo platform showcasing DevOps skills with AI-powered alert analysis.

**Stack:** Docker Compose → OpenTofu → GCP Cloud Run
**Status:** MVP Complete (v0.1.0)

## Quick Reference

```bash
# Start stack
docker-compose up -d

# Check status
docker-compose ps

# Test AI processor
curl http://localhost:8000/health

# View Grafana
open http://localhost:3000  # admin/admin123
```

## Key Files

| Component | Files |
|-----------|-------|
| Orchestration | `docker-compose.yml` |
| Prometheus | `monitoring/prometheus/prometheus.yml`, `alerts/rules.yml` |
| AI Processor | `ai-processor/app/main.py`, `llm_client.py` |
| Infrastructure | `infra/main.tf`, `variables.tf` |
| Status | `TODO.md`, `CHANGELOG.md` |

## Architecture Decisions

- **OpenTofu** over Terraform (CNCF-backed, open source)
- **GCP Cloud Run** for serverless (free tier friendly, scales to zero)
- **OpenAI GPT-4o-mini** for cost-effective analysis
- **FastAPI** for async webhook handling
- **Local-first** development, cloud deployment optional

## Session Workflow

1. Check `TODO.md` for current status
2. Run `docker-compose ps` to verify stack state
3. Make changes
4. Update `TODO.md` with progress
5. Update `CHANGELOG.md` for significant changes

## Constraints

- Keep within GCP free tier limits
- No secrets in git (use .env files, Secret Manager)
- OpenTofu syntax (not Terraform-specific features)
- Python 3.11+ for AI processor

## Common Tasks

### Add new alert rule
Edit: `monitoring/prometheus/alerts/rules.yml`

### Modify AI prompt
Edit: `ai-processor/app/llm_client.py` → `SYSTEM_PROMPT`

### Add Grafana datasource
Edit: `monitoring/grafana/provisioning/datasources/datasources.yml`

### Update Cloud Run config
Edit: `infra/main.tf` → `google_cloud_run_v2_service`
