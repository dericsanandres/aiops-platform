# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Grafana pre-built dashboards
- Slack/Discord notification channels
- CI/CD pipeline (GitHub Actions)
- Remote state backend (GCS)
- Full GCP deployment option

---

## [0.1.0] - 2024-12-30

### Added
- **Monitoring Stack**
  - Prometheus v2.50.0 with scrape configs
  - Grafana v10.3.0 with auto-provisioned datasources
  - Loki v2.9.0 for log aggregation
  - Alertmanager v0.27.0 with webhook routing
  - Promtail v2.9.0 for log shipping

- **Sample Workloads**
  - nginx with stub_status for metrics
  - node_exporter for host metrics
  - cAdvisor for container metrics

- **Alerting**
  - Basic alert rules (ContainerDown, HighCpuUsage, HighMemoryUsage)
  - Alertmanager webhook to AI Processor

- **AI Processor**
  - FastAPI application with `/webhook/alertmanager` endpoint
  - OpenAI integration (GPT-4o-mini)
  - Prometheus metrics endpoint
  - Health check endpoint

- **Infrastructure (OpenTofu)**
  - GCP Cloud Run service definition
  - Artifact Registry for container images
  - Secret Manager for API keys
  - Service account with minimal permissions

- **Documentation**
  - README with Mermaid architecture diagrams
  - Environment templates (.env.example, terraform.tfvars.example)
  - Project structure documentation

### Technical Decisions
- OpenTofu over Terraform (CNCF-backed, fully open source)
- GCP Cloud Run for serverless deployment (free tier friendly)
- OpenAI GPT-4o-mini for cost-effective AI analysis
- FastAPI for async webhook handling
- Docker Compose for local development

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 0.1.0 | 2024-12-30 | Initial MVP skeleton |

---

## Contributors

- Initial development by DevOps-Deric with Claude Code assistance
