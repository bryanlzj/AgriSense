# AgriSense - Docker Guide

**Purpose:** Complete guide to using Docker for AgriSense development and deployment  
**Audience:** Developers and DevOps engineers  
**Last Updated:** January 2025

---

## 📋 Table of Contents

1. [What is Docker?](#what-is-docker)
2. [Docker Architecture](#docker-architecture)
3. [Local Development with Docker](#local-development-with-docker)
4. [Docker Compose Services](#docker-compose-services)
5. [Common Docker Commands](#common-docker-commands)
6. [Debugging with Docker](#debugging-with-docker)
7. [Docker Best Practices](#docker-best-practices)

---

## 1. What is Docker?

**Docker** is a containerization platform that packages your application and all its dependencies into a standardized unit called a **container**.

### Why Use Docker?

✅ **Consistency:** "Works on my machine" → "Works everywhere"  
✅ **Isolation:** Each service runs in its own container  
✅ **Portability:** Deploy anywhere (local, VPS, cloud)  
✅ **Scalability:** Easy to scale services up/down  
✅ **Reproducibility:** Same environment for dev/staging/production  

### Docker vs Virtual Machines

| Feature | Docker Container | Virtual Machine |
|---------|-----------------|-----------------|
| **Size** | MBs | GBs |
| **Startup** | Seconds | Minutes |
| **Performance** | Native | Overhead |
| **Isolation** | Process-level | OS-level |
| **Resource Usage** | Lightweight | Heavy |

---

## 2. Docker Architecture

### AgriSense Docker Setup

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Host (Your Server)            │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │         Docker Network (agrisense-network)      │  │
│  │                                                 │  │
│  │  ┌──────────────┐      ┌──────────────┐       │  │
│  │  │   Backend    │      │  PostgreSQL  │       │  │
│  │  │  Container   │◄────►│  Container   │       │  │
│  │  │              │      │              │       │  │
│  │  │ FastAPI      │      │ Database     │       │  │
│  │  │ Port: 5000   │      │ Port: 5432   │       │  │
│  │  └──────┬───────┘      └──────┬───────┘       │  │
│  │         │                     │               │  │
│  │         │                     │               │  │
│  │  ┌──────▼──────────────────────▼────────┐    │  │
│  │  │         Docker Volumes               │    │  │
│  │  │  - postgres_data (database)          │    │  │
│  │  │  - uploads_data (images)             │    │  │
│  │  │  - logs_data (logs)                  │    │  │
│  │  └──────────────────────────────────────┘    │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  Exposed Ports:                                        │
│  - 5000 → Backend API                                  │
│  - 5432 → PostgreSQL (optional)                        │
└─────────────────────────────────────────────────────────┘
```

### Key Components

1. **Dockerfile** (`backend/Dockerfile`)
   - Instructions to build backend image
   - Multi-stage build for optimization
   - Non-root user for security

2. **Docker Compose** (`docker-compose.yml`)
   - Defines all services (backend, postgres)
   - Configures networks and volumes
   - Sets environment variables

3. **Docker Volumes**
   - Persistent storage for data
   - Survives container restarts
   - Shared between containers

4. **Docker Network**
   - Allows containers to communicate
   - Isolated from host network
   - DNS resolution between services

---

## 3. Local Development with Docker

### Option 1: Full Docker Setup (Recommended for Production Testing)

**Use Case:** Test production-like environment locally

```bash
# 1. Create .env file
cp .env.production.example .env
nano .env  # Configure environment variables

# 2. Start all services
docker-compose up -d

# 3. View logs
docker-compose logs -f backend

# 4. Access API
curl http://localhost:5000/health
open http://localhost:5000/docs

# 5. Stop services
docker-compose down
```

**Pros:**
- ✅ Identical to production
- ✅ Tests Docker configuration
- ✅ Includes PostgreSQL

**Cons:**
- ❌ Slower iteration (rebuild on code changes)
- ❌ More resource-intensive

---

### Option 2: Hybrid Setup (Recommended for Development)

**Use Case:** Fast development with local Python

```bash
# 1. Start only PostgreSQL in Docker
docker-compose up -d postgres

# 2. Run backend locally
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --reload --port 5000

# 3. Code changes auto-reload (no rebuild needed)
```

**Pros:**
- ✅ Fast iteration (hot reload)
- ✅ Easy debugging
- ✅ Uses real PostgreSQL

**Cons:**
- ❌ Requires Python installed locally
- ❌ Not identical to production

---

### Option 3: SQLite Only (Simplest for Quick Testing)

**Use Case:** Quick testing without Docker

```bash
# 1. Use SQLite (no Docker needed)
cd backend
source venv/bin/activate
export DATABASE_URL=sqlite:///./agrisense.db

# 2. Run migrations
alembic upgrade head

# 3. Start backend
uvicorn main:app --reload --port 5000
```

**Pros:**
- ✅ No Docker required
- ✅ Fastest setup
- ✅ Good for learning

**Cons:**
- ❌ SQLite limitations (no concurrent writes)
- ❌ Different from production

---

## 4. Docker Compose Services

### Backend Service

```yaml
backend:
  build: ./backend
  ports:
    - "5000:5000"
  environment:
    - DATABASE_URL=postgresql://...
    - SECRET_KEY=...
  volumes:
    - uploads_data:/app/uploads
    - logs_data:/app/logs
  depends_on:
    - postgres
```

**Key Points:**
- Built from `backend/Dockerfile`
- Exposes port 5000 to host
- Mounts volumes for persistent data
- Waits for PostgreSQL to be ready

---

### PostgreSQL Service

```yaml
postgres:
  image: postgres:15-alpine
  environment:
    - POSTGRES_USER=agrisense_user
    - POSTGRES_PASSWORD=...
    - POSTGRES_DB=agrisense
  volumes:
    - postgres_data:/var/lib/postgresql/data
  ports:
    - "5432:5432"
```

**Key Points:**
- Uses official PostgreSQL image
- Data persists in `postgres_data` volume
- Port 5432 exposed (optional, for debugging)
- Health check ensures database is ready

---

## 5. Common Docker Commands

### Service Management

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d postgres

# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ deletes data!)
docker-compose down -v

# Restart services
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Viewing Logs

```bash
# View all logs
docker-compose logs

# View backend logs only
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f backend

# View last 100 lines
docker-compose logs --tail=100 backend

# View logs with timestamps
docker-compose logs -t backend
```

### Checking Status

```bash
# List running containers
docker-compose ps

# Check container details
docker inspect agrisense-backend

# Check resource usage
docker stats

# Check disk usage
docker system df
```

### Executing Commands in Containers

```bash
# Run command in backend container
docker-compose exec backend <command>

# Examples:
docker-compose exec backend alembic upgrade head
docker-compose exec backend alembic current
docker-compose exec backend python scripts/seed_data.py

# Access backend shell
docker-compose exec backend bash

# Access PostgreSQL shell
docker-compose exec postgres psql -U agrisense_user agrisense
```

### Building and Rebuilding

```bash
# Build images
docker-compose build

# Build without cache (clean build)
docker-compose build --no-cache

# Rebuild and restart
docker-compose up -d --build

# Pull latest base images
docker-compose pull
```

### Cleaning Up

```bash
# Remove stopped containers
docker-compose rm

# Remove all unused images
docker image prune -a

# Remove all unused volumes
docker volume prune

# Remove everything (⚠️ nuclear option)
docker system prune -a --volumes
```

---

## 6. Debugging with Docker

### Problem: Backend won't start

**Check logs:**
```bash
docker-compose logs backend
```

**Common errors:**

1. **Port already in use:**
   ```
   Error: bind: address already in use
   ```
   **Solution:** Stop other service using port 5000
   ```bash
   sudo lsof -i :5000
   sudo kill -9 <PID>
   ```

2. **Database connection failed:**
   ```
   could not connect to server
   ```
   **Solution:** Wait for PostgreSQL to be ready
   ```bash
   docker-compose logs postgres
   docker-compose restart backend
   ```

3. **Missing environment variables:**
   ```
   KeyError: 'SECRET_KEY'
   ```
   **Solution:** Check `.env` file exists and is configured

---

### Problem: Database not persisting data

**Check volumes:**
```bash
docker volume ls
docker volume inspect agrisense_postgres_data
```

**Solution:** Ensure volume is mounted correctly in `docker-compose.yml`

---

### Problem: Out of disk space

**Check disk usage:**
```bash
docker system df
```

**Clean up:**
```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove build cache
docker builder prune
```

---

### Problem: Slow performance

**Check resource usage:**
```bash
docker stats
```

**Solutions:**
- Increase Docker memory limit (Docker Desktop settings)
- Use multi-stage builds to reduce image size
- Optimize Dockerfile (fewer layers, smaller base image)

---

## 7. Docker Best Practices

### Security

✅ **Use non-root user in containers**
```dockerfile
RUN useradd -m -u 1000 agrisense
USER agrisense
```

✅ **Don't store secrets in Dockerfile**
```dockerfile
# ❌ Bad
ENV SECRET_KEY=abc123

# ✅ Good - use .env file
ENV SECRET_KEY=${SECRET_KEY}
```

✅ **Use specific image versions**
```dockerfile
# ❌ Bad
FROM python:3

# ✅ Good
FROM python:3.10-slim
```

---

### Performance

✅ **Use multi-stage builds**
```dockerfile
FROM python:3.10-slim as builder
# Build dependencies

FROM python:3.10-slim
# Copy only what's needed
```

✅ **Minimize layers**
```dockerfile
# ❌ Bad (3 layers)
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# ✅ Good (1 layer)
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean
```

✅ **Use .dockerignore**
```
# Exclude unnecessary files
__pycache__/
*.pyc
.git/
tests/
```

---

### Maintainability

✅ **Use health checks**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:5000/health || exit 1
```

✅ **Label your images**
```dockerfile
LABEL maintainer="your-email@example.com"
LABEL version="1.0.0"
LABEL description="AgriSense Backend API"
```

✅ **Document your Dockerfile**
```dockerfile
# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev
```

---

## 8. Docker Compose Tips

### Override for Development

Create `docker-compose.override.yml` for local development:

```yaml
version: '3.8'

services:
  backend:
    volumes:
      - ./backend:/app  # Mount code for hot reload
    environment:
      - DEBUG=True
    command: uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

This file is automatically merged with `docker-compose.yml`.

---

### Multiple Environments

```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

---

### Environment Variables

**Priority (highest to lowest):**
1. Command line: `docker-compose run -e VAR=value`
2. Shell environment: `export VAR=value`
3. `.env` file
4. `docker-compose.yml` environment section
5. Dockerfile `ENV` instruction

---

## 9. Quick Reference

### Cheat Sheet

| Task | Command |
|------|---------|
| Start services | `docker-compose up -d` |
| Stop services | `docker-compose down` |
| View logs | `docker-compose logs -f backend` |
| Rebuild | `docker-compose up -d --build` |
| Run migrations | `docker-compose exec backend alembic upgrade head` |
| Access shell | `docker-compose exec backend bash` |
| Check status | `docker-compose ps` |
| Clean up | `docker system prune -a` |

---

## 10. Learning Resources

- **Official Docker Docs:** https://docs.docker.com/
- **Docker Compose Docs:** https://docs.docker.com/compose/
- **Best Practices:** https://docs.docker.com/develop/dev-best-practices/
- **Dockerfile Reference:** https://docs.docker.com/engine/reference/builder/

---

**End of Docker Guide**

*For deployment instructions, see `DEPLOYMENT_GUIDE.md`*
