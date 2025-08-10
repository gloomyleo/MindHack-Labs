# One-command Lab with Docker Compose

This stack runs:
- Postgres (for n8n)
- n8n (workflow engine)
- Three local APIs (deepfake, redteam, pqc)
- Grafana (optional dashboards)

## Prereqs
- Docker Desktop or Docker Engine + docker-compose
- (Optional) `OPENAI_API_KEY` for the Red Team planner

## Run
```bash
# from repo root
docker compose build
OPENAI_API_KEY=your_key_here docker compose up -d
# Open n8n:     http://localhost:5678
# Grafana:      http://localhost:3000  (admin/admin)
# Deepfake API: http://localhost:5001/detect
# RedTeam API:  http://localhost:5002/simulate
# PQC API:      http://localhost:5003/benchmark
```

## Stop
```bash
docker compose down
```

## Notes
- Update HTTP Request nodes in n8n to use `http://api_deepfake:5001`, `http://api_redteam:5002`, `http://api_pqc:5003` **inside** Docker.
- When testing from your host browser or Postman, use `http://localhost:<port>`.
