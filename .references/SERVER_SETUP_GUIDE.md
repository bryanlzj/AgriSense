# AgriSense Server Setup Guide - From Scratch

**Target:** Fresh Ubuntu server → Fully deployed AgriSense backend  
**Time Required:** ~30-45 minutes  
**Skill Level:** Beginner-friendly with copy-paste commands

---

## 📋 Prerequisites

- ✅ Ubuntu server (20.04 or 22.04 recommended)
- ✅ SSH access to the server
- ✅ Root or sudo privileges
- ✅ Server public IP address
- ✅ Domain name (optional, but recommended for SSL)

---

## 🚀 Step-by-Step Setup

### Step 1: Connect to Your Server

```bash
# From your local machine, connect via SSH
ssh root@YOUR_SERVER_IP

# Or if you have a non-root user:
ssh username@YOUR_SERVER_IP
```

---

### Step 2: Update System Packages

```bash
# Update package list
sudo apt update

# Upgrade installed packages
sudo apt upgrade -y

# Install basic utilities
sudo apt install -y curl wget git nano ufw
```

**Expected time:** 2-5 minutes

---

### Step 3: Install Docker

```bash
# Remove old Docker versions (if any)
sudo apt remove docker docker-engine docker.io containerd runc

# Install prerequisites
sudo apt install -y ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify Docker installation
sudo docker --version
sudo docker compose version
```

**Expected output:**
```
Docker version 24.x.x
Docker Compose version v2.x.x
```

**Expected time:** 3-5 minutes

---

### Step 4: Configure Docker (Optional but Recommended)

```bash
# Add your user to docker group (to run docker without sudo)
sudo usermod -aG docker $USER

# Apply group changes (or logout and login again)
newgrp docker

# Test Docker without sudo
docker run hello-world
```

**Expected output:** "Hello from Docker!" message

---

### Step 5: Configure Firewall

```bash
# Enable UFW firewall
sudo ufw enable

# Allow SSH (IMPORTANT: Do this first!)
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow backend port (optional, for direct access)
sudo ufw allow 5000/tcp

# Check firewall status
sudo ufw status
```

**Expected output:**
```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
5000/tcp                   ALLOW       Anywhere
```

---

### Step 6: Clone Your Repository

```bash
# Navigate to home directory
cd ~

# Clone the AgriSense repository
# Replace with your actual repository URL
git clone https://github.com/YOUR_USERNAME/agrisense.git

# Navigate to project directory
cd agrisense

# Verify files
ls -la
```

**Expected output:** You should see `backend/`, `docker-compose.yml`, etc.

**Note:** If your repository is private, you'll need to:
```bash
# Option 1: Use HTTPS with personal access token
git clone https://YOUR_TOKEN@github.com/YOUR_USERNAME/agrisense.git

# Option 2: Set up SSH key (recommended)
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub  # Add this to GitHub
git clone git@github.com:YOUR_USERNAME/agrisense.git
```

---

### Step 7: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.production.example .env

# Edit the environment file
nano .env
```

**Configure these critical values:**

```bash
# 1. GENERATE A SECURE SECRET KEY
# Run this command to generate:
openssl rand -hex 32

# Copy the output and paste it in .env as:
SECRET_KEY=your_generated_secret_key_here

# 2. SET SECURE DATABASE PASSWORD
POSTGRES_PASSWORD=your_secure_database_password_here

# 3. WEATHER API - No key required!
# Uses Open-Meteo API which is free and needs no API key

# 4. SET YOUR DOMAIN (if you have one)
CORS_ORIGINS=["http://YOUR_SERVER_IP:5000","https://yourdomain.com"]

# 5. VERIFY OTHER SETTINGS
ENVIRONMENT=production
DEBUG=false
```

**Save and exit nano:**
- Press `Ctrl + X`
- Press `Y` to confirm
- Press `Enter` to save

**Verify your .env file:**
```bash
cat .env | grep -E "SECRET_KEY|POSTGRES_PASSWORD|OPENROUTER_API_KEY"
```

Make sure none of these show the example values!

---

### Step 8: Deploy AgriSense

```bash
# Make deployment script executable
chmod +x backend/scripts/deploy.sh

# Run the deployment script
./backend/scripts/deploy.sh production
```

**The script will automatically:**
1. ✅ Check prerequisites (Docker, Docker Compose, .env)
2. ✅ Stop any running containers
3. ✅ Build Docker images
4. ✅ Start PostgreSQL database
5. ✅ Start FastAPI backend
6. ✅ Wait for database to be ready
7. ✅ Run database migrations
8. ✅ Verify deployment health

**Expected time:** 5-10 minutes (first time, includes image building)

**Expected output:**
```
========================================
  AgriSense Deployment Script
========================================

[✓] Docker is installed
[✓] Docker Compose is installed
[✓] .env file exists

Stopping running containers...
Building Docker images...
Starting services...
Waiting for database to be ready...
Running database migrations...

========================================
  Deployment Successful! ✓
========================================

Backend: http://YOUR_SERVER_IP:5000
API Docs: http://YOUR_SERVER_IP:5000/docs
Health: http://YOUR_SERVER_IP:5000/health
```

---

### Step 9: Verify Deployment

```bash
# Check running containers
docker ps

# Expected output: 2 containers running (backend, postgres)

# Check backend logs
docker compose logs -f backend

# Press Ctrl+C to exit logs

# Test health endpoint
curl http://localhost:5000/health

# Expected output: {"status":"healthy"}

# Test from your local machine (replace YOUR_SERVER_IP)
curl http://YOUR_SERVER_IP:5000/health
```

**Access API Documentation:**
- Open browser: `http://YOUR_SERVER_IP:5000/docs`
- You should see the Swagger UI with all API endpoints

---

### Step 10: Create First Admin User (Optional)

```bash
# Access the backend container
docker compose exec backend bash

# Inside the container, create admin user
python -c "
from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

db = SessionLocal()
admin = User(
    username='admin',
    hashed_password=get_password_hash('admin123'),
    role='admin'
)
db.add(admin)
db.commit()
print('Admin user created: username=admin, password=admin123')
db.close()
"

# Exit container
exit
```

**Test login:**
```bash
curl -X POST "http://YOUR_SERVER_IP:5000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**Expected output:** JSON with `access_token`

---

## 🔧 Post-Deployment Tasks

### Set Up Automated Backups

```bash
# Make backup script executable
chmod +x backend/scripts/backup.sh

# Test backup manually
./backend/scripts/backup.sh

# Set up daily automated backups with cron
crontab -e

# Add this line (daily backup at 2 AM):
0 2 * * * cd ~/agrisense && ./backend/scripts/backup.sh >> ~/agrisense/logs/backup.log 2>&1
```

---

### Monitor Your Application

```bash
# View all container logs
docker compose logs -f

# View only backend logs
docker compose logs -f backend

# View only database logs
docker compose logs -f postgres

# Check container resource usage
docker stats

# Check disk usage
df -h
```

---

### Restart Services

```bash
# Restart all services
docker compose restart

# Restart only backend
docker compose restart backend

# Stop all services
docker compose down

# Start all services
docker compose up -d
```

---

## 🌐 Optional: Set Up Domain & SSL (Recommended for Production)

If you have a domain name (e.g., `api.agrisense.com`):

### 1. Point Domain to Server

In your domain registrar (GoDaddy, Namecheap, etc.):
- Create an **A record** pointing to your server IP
- Wait 5-10 minutes for DNS propagation

### 2. Install Nginx

```bash
sudo apt install -y nginx
```

### 3. Configure Nginx as Reverse Proxy

```bash
sudo nano /etc/nginx/sites-available/agrisense
```

**Paste this configuration:**

```nginx
server {
    listen 80;
    server_name api.agrisense.com;  # Replace with your domain

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable the site:**

```bash
sudo ln -s /etc/nginx/sites-available/agrisense /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Install SSL Certificate (Free with Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d api.agrisense.com

# Follow the prompts:
# - Enter your email
# - Agree to terms
# - Choose to redirect HTTP to HTTPS (recommended)
```

**Your API is now available at:**
- `https://api.agrisense.com/docs` (Swagger UI)
- `https://api.agrisense.com/health` (Health check)

**SSL certificate auto-renewal:**
```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot automatically sets up a cron job for renewal
```

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to Docker daemon"

```bash
# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Check Docker status
sudo systemctl status docker
```

---

### Issue: "Port 5000 already in use"

```bash
# Find what's using port 5000
sudo lsof -i :5000

# Kill the process (replace PID with actual process ID)
sudo kill -9 PID

# Or change the port in docker-compose.yml
```

---

### Issue: "Database connection failed"

```bash
# Check if PostgreSQL container is running
docker ps | grep postgres

# Check PostgreSQL logs
docker compose logs postgres

# Restart database
docker compose restart postgres

# Wait 10 seconds and try again
sleep 10
curl http://localhost:5000/health
```

---

### Issue: "Migration failed"

```bash
# Access backend container
docker compose exec backend bash

# Check current migration version
alembic current

# Try upgrading manually
alembic upgrade head

# If errors persist, check logs
alembic history
exit
```

---

### Issue: "Out of disk space"

```bash
# Check disk usage
df -h

# Clean up Docker
docker system prune -a --volumes

# Remove old backups (keep last 7 days)
find ~/agrisense/backups -name "*.sql.gz" -mtime +7 -delete
```

---

## 📊 Quick Reference Commands

```bash
# View running containers
docker ps

# View all logs
docker compose logs -f

# Restart backend
docker compose restart backend

# Stop all services
docker compose down

# Start all services
docker compose up -d

# Run backup
./backend/scripts/backup.sh

# Check health
curl http://localhost:5000/health

# Access API docs
# Browser: http://YOUR_SERVER_IP:5000/docs

# Update code and redeploy
git pull origin main
./backend/scripts/deploy.sh production
```

---

## ✅ Deployment Checklist

- [ ] Ubuntu server with SSH access
- [ ] System packages updated
- [ ] Docker and Docker Compose installed
- [ ] Firewall configured (ports 22, 80, 443, 5000)
- [ ] Repository cloned
- [ ] .env file configured with secure values
- [ ] SECRET_KEY generated (32-byte hex)
- [ ] POSTGRES_PASSWORD set (strong password)
- [x] Weather API: Uses Open-Meteo (no key required)
- [ ] Deployment script executed successfully
- [ ] Health endpoint responding
- [ ] API documentation accessible
- [ ] Admin user created (optional)
- [ ] Automated backups configured
- [ ] Domain pointed to server (optional)
- [ ] SSL certificate installed (optional)

---

## 🎯 Success Criteria

Your deployment is successful when:

✅ `docker ps` shows 2 running containers (backend, postgres)  
✅ `curl http://localhost:5000/health` returns `{"status":"healthy"}`  
✅ Browser shows Swagger UI at `http://YOUR_SERVER_IP:5000/docs`  
✅ You can create users and login via API  
✅ Database migrations completed successfully  

---

## 📞 Need Help?

If you encounter issues:

1. **Check logs:** `docker compose logs -f backend`
2. **Check container status:** `docker ps -a`
3. **Verify .env file:** `cat .env | grep -v "^#" | grep -v "^$"`
4. **Check firewall:** `sudo ufw status`
5. **Test database:** `docker compose exec postgres psql -U agrisense -d agrisense -c "\dt"`

---

## 🎉 Next Steps After Deployment

1. **Test all API endpoints** in Swagger UI
2. **Create test users** and verify authentication
3. **Add sensor data** and test weather/pest endpoints
4. **Set up monitoring** (optional: install Prometheus/Grafana)
5. **Configure mobile app** to connect to your server
6. **Set up CI/CD** (optional: GitHub Actions for auto-deploy)

---

**Deployment Guide Version:** 1.0  
**Last Updated:** January 4, 2025  
**Tested On:** Ubuntu 22.04 LTS

---

**Ready to deploy? Start with Step 1! 🚀**
