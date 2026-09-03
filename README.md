# Task Manager — Dockerized Multi-Container App

A simple task management REST API built to practice Docker Compose, multi-stage builds, Nginx reverse proxy, cloud deployment, and CI/CD automation.

## Tech Stack

- **Backend:** Python (Flask)
- **Database:** PostgreSQL
- **Reverse Proxy:** Nginx
- **Containerization:** Docker, Docker Compose (multi-stage builds)
- **Deployment:** AWS EC2
- **CI/CD:** GitHub Actions

## Architecture


Nginx acts as the single entry point and reverse-proxies all `/api/` requests to the Flask backend. The backend and database are not exposed directly — only Nginx is reachable from outside the Docker network.

## Features

- CRUD API for tasks (create, list, delete)
- Multi-stage Dockerfile for a lean production image
- Docker Compose orchestration with healthchecks (backend waits for Postgres to be *actually* ready, not just started)
- Data persistence via named volumes
- Automated deployment via GitHub Actions — every push to `main` automatically SSHes into the EC2 server, pulls the latest code, and rebuilds the containers

## API Endpoints

| Method | Endpoint          | Description        |
|--------|-------------------|---------------------|
| GET    | `/api/health`     | Health check        |
| GET    | `/api/tasks`      | List all tasks      |
| POST   | `/api/tasks`      | Create a new task    |
| DELETE | `/api/tasks/<id>` | Delete a task        |

## CI/CD Pipeline

On every push to `main`, a GitHub Actions workflow (`.github/workflows/deploy.yml`) automatically:
1. Connects to the EC2 instance via SSH
2. Pulls the latest code (`git pull`)
3. Rebuilds and restarts the containers (`docker compose up --build -d`)

No manual deployment steps required after the initial server setup.

## Running Locally

```bash
git clone https://github.com/Harshpoddar1/task-manager-docker.git
cd task-manager-docker
docker compose up --build
```

App will be available at `http://localhost/api/health`

## What I Learned

- `depends_on` in Docker Compose only controls container **start order** — it doesn't guarantee a service is actually ready to accept connections. Hit a real race condition where Flask tried connecting to Postgres before it had finished initializing. Fixed it by adding a proper `healthcheck` on the database service and using `condition: service_healthy`.
- GitHub Actions runners connect from dynamic IPs, not a fixed one — so restricting SSH (port 22) to a single "My IP" in the security group blocks the CI/CD pipeline itself.
- Personal Access Tokens need the `workflow` scope specifically to push changes to `.github/workflows/` files — the default `repo` scope isn't enough.
