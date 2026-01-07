# AgriSense - Deployment Guide

**Version:** 1.0  
**Last Updated:** January 2025  
**Target Environment:** Production Server (Docker + PostgreSQL)

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Server Setup](#server-setup)
3. [Initial Deployment](#initial-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Database Management](#database-management)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)
8. [Backup & Restore](#backup--restore)

---

## 1. Prerequisites

### Server Requirements

**Minimum Specifications:**
- **OS:** Ubuntu 20.04 LTS or later
- **CPU:** 2 cores
- **RAM:** 4GB
- **Storage:** 20GB SSD
- **Network:** Public IP address with open ports 80, 443, 5000

**Recommended Specifications:**
- **OS:** Ubuntu 22.04 LTS
- **CPU:** 4 cores
- **RAM:** 8GB
- **Storage:** 50GB SSD

### Software Requirements

- **Docker:** Version 20.10 or later
- **Docker Compose:** Version 2.0 or later
- **Git:** For code deployment
- **SSL Certificate:** Let's Encrypt (free)

---

## 2. Server Setup

### Step 1: Update System

```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y curl git wget nano ufw
```

### Step 2: Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add current user to docker group
sudo usermod -aG docker $USER

# Start Docker service
sudo systemctl enable docker
sudo systemctl start docker

# Verify installation
docker --version
```

### Step 3: Install Docker Compose

```bash
# Download Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

### Step 4: Configure Firewall

```bash
# Enable UFW firewall
sudo ufw enable

# Allow SSH (important!)
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow backend API (optional, if not using reverse proxy)
sudo ufw allow 5000/tcp

# Check firewall status
sudo ufw status
```

### Step 5: Create Application Directory

```bash
# Create directory for application
sudo mkdir -p /opt/agrisense
sudo chown $USER:$USER /opt/agrisense
cd /opt/agrisense
```

---

## 3. Initial Deployment

### Step 1: Clone Repository

```bash
# Clone the repository
cd /opt/agrisense
git clone https://github.com/yourusername/agrisense.git .

# Or upload files manually via SCP/SFTP
```

### Step 2: Configure Environment

```bash
# Copy production environment template
cp .env.production.example .env

# Edit environment variables
nano .env
```

**Required Configuration:**

```bash
# Database
POSTGRES_USER=agrisense_user
POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD_HERE  # Change this!
POSTGRES_DB=agrisense

# Security
SECRET_KEY=YOUR_SECRET_KEY_HERE  # Generate with: openssl rand -hex 32

# Weather API
OPENWEATHER_API_KEY=your_openweather_api_key_here

# CORS (add your domain)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Generate Secure Secret Key:**

```bash
openssl rand -hex 32
```

### Step 3: Deploy Application

```bash
# Make deployment script executable
chmod +x backend/scripts/deploy.sh

# Run deployment
./backend/scripts/deploy.sh production
```

The deployment script will:
1. ✅ Check prerequisites (Docker, Docker Compose)
2. ✅ Build Docker images
3. ✅ Start services (PostgreSQL + Backend)
4. ✅ Wait for database to be ready
5. ✅ Run database migrations
6. ✅ Verify deployment

### Step 4: Verify Deployment

```bash
# Check running containers
docker-compose ps

# Check backend logs
docker-compose logs -f backend

# Test health endpoint
curl http://localhost:5000/health

# Test API documentation
curl http://localhost:5000/docs
```

**Expected Output:**

```json
{
  "status": "healthy",
  "timestamp": "2025-01-04T10:30:00Z",
  "database": "connected",
  "version": "1.0.0"
}
```

---

## 4. Environment Configuration

### Production Environment Variables

**Critical Settings:**

| Variable | Description | Example |
|----------|-------------|---------|
| `POSTGRES_PASSWORD` | Database password | `SecurePass123!` |
| `SECRET_KEY` | JWT secret key | `abc123...` (64 chars) |
| `OPENWEATHER_API_KEY` | Weather API key | `your_api_key` |
| `CORS_ORIGINS` | Allowed frontend URLs | `https://yourdomain.com` |
| `DEBUG` | Debug mode (False in prod) | `False` |
| `ENVIRONMENT` | Environment name | `production` |

### Optional Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `LOG_LEVEL` | Logging level | `INFO` |
| `USE_MOCK_ML` | Use mock ML service | `True` |
| `ML_SERVICE_URL` | Real ML service URL | `http://ml-service:8001` |

---

## 5. Database Management

### Run Migrations

```bash
# Run all pending migrations
docker-compose exec backend alembic upgrade head

# Check current migration version
docker-compose exec backend alembic current

# View migration history
docker-compose exec backend alembic history
```

### Rollback Migrations

```bash
# Rollback last migration
./backend/scripts/rollback.sh 1

# Rollback multiple migrations
./backend/scripts/rollback.sh 3
```

### Create New Migration

```bash
# Auto-generate migration from model changes
docker-compose exec backend alembic revision --autogenerate -m "Add new field to users table"

# Review generated migration
nano backend/alembic/versions/XXXX_add_new_field.py

# Apply migration
docker-compose exec backend alembic upgrade head
```

---

## 6. Monitoring & Maintenance

### View Logs

```bash
# View all logs
docker-compose logs

# View backend logs only
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f backend

# View last 100 lines
docker-compose logs --tail=100 backend
```

### Check Service Status

```bash
# Check all services
docker-compose ps

# Check backend health
curl http://localhost:5000/health

# Check database connection
docker-compose exec postgres pg_isready -U agrisense_user
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart backend only
docker-compose restart backend

# Restart database only
docker-compose restart postgres
```

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
./backend/scripts/deploy.sh production
```

---

## 7. Troubleshooting

### Backend Won't Start

**Symptom:** Backend container exits immediately

**Solution:**

```bash
# Check logs for errors
docker-compose logs backend

# Common issues:
# 1. Database not ready - wait 30 seconds and retry
# 2. Missing environment variables - check .env file
# 3. Port already in use - check: sudo lsof -i :5000
```

### Database Connection Failed

**Symptom:** `could not connect to server`

**Solution:**

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres

# Verify connection
docker-compose exec postgres psql -U agrisense_user -d agrisense -c "SELECT 1;"
```

### Migration Errors

**Symptom:** `alembic.util.exc.CommandError`

**Solution:**

```bash
# Check current migration state
docker-compose exec backend alembic current

# Check migration history
docker-compose exec backend alembic history

# If stuck, stamp to specific version
docker-compose exec backend alembic stamp head

# Then retry migration
docker-compose exec backend alembic upgrade head
```

### Out of Disk Space

**Symptom:** `no space left on device`

**Solution:**

```bash
# Check disk usage
df -h

# Clean Docker images and containers
docker system prune -a --volumes

# Remove old logs
docker-compose exec backend rm -rf /app/logs/*.log

# Check database size
docker-compose exec postgres psql -U agrisense_user -d agrisense -c "SELECT pg_size_pretty(pg_database_size('agrisense'));"
```

### High Memory Usage

**Symptom:** Server becomes slow or unresponsive

**Solution:**

```bash
# Check memory usage
free -h

# Check Docker container memory
docker stats

# Restart services to free memory
docker-compose restart

# If persistent, upgrade server RAM
```

---

## 8. Backup & Restore

### Create Backup

```bash
# Create database backup
./backend/scripts/backup.sh

# Backup is saved to: backups/agrisense_backup_YYYYMMDD_HHMMSS.sql.gz
```

**Backup Schedule (Recommended):**

```bash
# Add to crontab for daily backups at 2 AM
crontab -e

# Add this line:
0 2 * * * cd /opt/agrisense && ./backend/scripts/backup.sh >> /var/log/agrisense_backup.log 2>&1
```

### Restore Backup

```bash
# List available backups
ls -lh backups/

# Restore specific backup
./backend/scripts/restore.sh backups/agrisense_backup_20250104_120000.sql.gz
```

### Manual Backup (Alternative)

```bash
# Export database
docker-compose exec -T postgres pg_dump -U agrisense_user agrisense > backup.sql

# Compress backup
gzip backup.sql

# Download backup to local machine
scp user@server:/opt/agrisense/backup.sql.gz ./
```

### Manual Restore (Alternative)

```bash
# Upload backup to server
scp backup.sql.gz user@server:/opt/agrisense/

# Decompress
gunzip backup.sql.gz

# Restore database
cat backup.sql | docker-compose exec -T postgres psql -U agrisense_user agrisense
```

---

## 9. SSL/HTTPS Setup (Optional but Recommended)

### Using Nginx Reverse Proxy + Let's Encrypt

**Step 1: Install Nginx**

```bash
sudo apt install -y nginx
```

**Step 2: Configure Nginx**

```bash
sudo nano /etc/nginx/sites-available/agrisense
```

**Nginx Configuration:**

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable Site:**

```bash
sudo ln -s /etc/nginx/sites-available/agrisense /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Step 3: Install SSL Certificate**

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
```

---

## 10. Production Checklist

Before going live, verify:

- [ ] `.env` file configured with secure passwords
- [ ] `SECRET_KEY` generated with `openssl rand -hex 32`
- [ ] `DEBUG=False` in production
- [ ] `CORS_ORIGINS` set to your domain
- [ ] OpenWeatherMap API key configured
- [ ] Firewall configured (ports 80, 443, 22 only)
- [ ] SSL certificate installed
- [ ] Database backups scheduled (cron job)
- [ ] Health check endpoint working
- [ ] API documentation accessible
- [ ] Logs being written to `/app/logs/`
- [ ] Disk space monitored
- [ ] Server monitoring set up (optional: Uptime Robot, Pingdom)

---

## 11. Quick Reference Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend

# Restart backend
docker-compose restart backend

# Run migrations
docker-compose exec backend alembic upgrade head

# Create backup
./backend/scripts/backup.sh

# Restore backup
./backend/scripts/restore.sh backups/backup_file.sql.gz

# Check health
curl http://localhost:5000/health

# Access database
docker-compose exec postgres psql -U agrisense_user agrisense
```

---

## 12. Support & Resources

- **Documentation:** `/docs` folder
- **API Docs:** `http://your-server:5000/docs`
- **GitHub Issues:** Report bugs and request features
- **Email Support:** your-email@example.com

---

**End of Deployment Guide**

*For development setup, see `backend/README.md`*
