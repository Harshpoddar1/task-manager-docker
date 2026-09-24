# Task Manager — Dockerized Multi-Container App with DevSecOps Pipeline

A task management REST API built to practice Docker Compose, multi-stage builds, Nginx reverse proxy, cloud deployment, and a full DevSecOps pipeline (secrets management, vulnerability scanning, IaC, monitoring, and PR-based deployment).

## Tech Stack

- **Backend:** Python (Flask)
- **Database:** PostgreSQL
- **Reverse Proxy:** Nginx
- **Containerization:** Docker, Docker Compose (multi-stage builds)
- **Infrastructure as Code:** Terraform (provisions EC2 + security group on AWS)
- **CI/CD:** GitHub Actions
- **Security Scanning:** Trivy (container images), pip-audit (Python dependencies)
- **Monitoring:** Uptime Kuma

## Architecture

Nginx is the single entry point and reverse-proxies `/api/` requests to Flask. Backend and database are never exposed directly. Uptime Kuma runs as a sibling container polling the backend's health endpoint.

## Features

- CRUD API for tasks (create, list, delete)
- Multi-stage Dockerfile for a lean production image
- Docker Compose orchestration with healthchecks (backend waits for Postgres to be *actually* ready)
- No hardcoded secrets — DB credentials injected via `.env` locally and GitHub Secrets in CI/CD
- Automated deployment via GitHub Actions on every push to `main`
- Container image scanning (Trivy) with a custom policy: fails the build only on fixable CRITICAL/HIGH vulnerabilities, warns on unfixable ones, ignores MEDIUM/LOW
- Dependency vulnerability scanning (pip-audit) as a separate, faster pre-build gate
- Infrastructure provisioned via Terraform instead of manual console clicks
- Live uptime monitoring and downtime history via Uptime Kuma
- Branch protection on `main` — all changes go through a pull request, no direct pushes

## API Endpoints

| Method | Endpoint          | Description        |
|--------|-------------------|---------------------|
| GET    | `/api/health`     | Health check        |
| GET    | `/api/tasks`      | List all tasks      |
| POST   | `/api/tasks`      | Create a new task    |
| DELETE | `/api/tasks/<id>` | Delete a task        |

## CI/CD Pipeline

On every push to `main`:
1. Checkout code
2. Run `pip-audit` against `requirements.txt`
3. Build the backend Docker image
4. Trivy scan (visibility pass — never blocks)
5. Trivy scan (gate — fails only on fixable CRITICAL/HIGH)
6. SSH into the EC2 server, pull latest code, regenerate `.env` from GitHub Secrets, rebuild and restart containers

## Infrastructure

EC2 instance and security group are defined in `terraform/main.tf` and provisioned with `terraform apply` instead of manual AWS Console setup.

## Running Locally

```bash
git clone https://github.com/Harshpoddar1/task-manager-docker.git
cd task-manager-docker
docker compose up --build
```

App: `http://localhost/api/health` · Monitoring dashboard: `http://localhost:1067`

## What I Learned

- `depends_on` only controls container **start order**, not readiness — fixed a real race condition between Flask and Postgres with a proper `healthcheck`.
- A secret committed to git is compromised forever, even if removed later — prevention (`.gitignore` + secret managers) is the only real fix.
- A Docker image carries far more than your own code — base OS packages and even a library's own bundled/vendored dependencies (like `setuptools`'s internal copy of `wheel`) can carry CVEs you never installed directly.
- "Latest" versions aren't a permanent fix — chasing every new CVE is an infinite loop; real teams manage risk with severity thresholds and accepted-risk exceptions instead of demanding zero vulnerabilities.
- GitHub Actions runners connect from dynamic IPs, not a fixed one — restricting SSH to "My IP" in the security group blocks the pipeline itself.
- GitHub repo admins can bypass their own branch protection rules by default — has to be explicitly disabled to actually enforce PR-only merges.
