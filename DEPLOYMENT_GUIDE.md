# Deployment Guide - Laboratory Information System

This guide covers various deployment options for your LIS application, from easiest to more advanced.

---

## Table of Contents

1. [Quick Start: Docker Deployment (Local)](#1-quick-start-docker-deployment-local)
2. [Free Tier Options](#2-free-tier-options)
   - [Render.com](#option-1-rendercom-easiest)
   - [Railway.app](#option-2-railwayapp)
   - [Fly.io](#option-3-flyio)
3. [Cloud Platforms](#3-cloud-platforms)
   - [AWS (EC2, ECS, Elastic Beanstalk)](#aws-options)
   - [Google Cloud Platform](#google-cloud-platform)
   - [Microsoft Azure](#microsoft-azure)
4. [Traditional VPS](#4-traditional-vps-digitalocean-linode-etc)
5. [Platform-as-a-Service (PaaS)](#5-platform-as-a-service-paas)
   - [Heroku](#heroku)
   - [DigitalOcean App Platform](#digitalocean-app-platform)

---

## 1. Quick Start: Docker Deployment (Local)

### Prerequisites
- Docker installed on your machine
- Your code repository

### Steps

```bash
# 1. Clone or navigate to your repository
cd Labtestmanagement

# 2. Build the Docker image
docker build -t lis:latest .

# 3. Run the container
docker run -d -p 5000:5000 --name lis-app \
  -v $(pwd)/data:/app/data \
  lis:latest

# 4. Access the application
# Open browser: http://localhost:5000
```

### Useful Commands
```bash
# View logs
docker logs lis-app

# Stop container
docker stop lis-app

# Remove container
docker rm lis-app

# Restart container
docker restart lis-app
```

---

## 2. Free Tier Options

### Option 1: Render.com (Easiest)

**Why Render?**
- Free tier available
- Automatic deployments from GitHub
- Built-in Docker support
- Free SSL certificates
- Simple setup

#### Steps:

1. **Prepare Your Repository**
   - Push your code to GitHub (already done ✓)

2. **Sign Up for Render**
   - Go to https://render.com
   - Sign up with GitHub account

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `Labtest-Management`
   - Configure settings:
     - **Name:** `lis-app` (or any name)
     - **Region:** Choose closest to you
     - **Branch:** `main`
     - **Root Directory:** Leave blank (root)
     - **Environment:** `Docker`
     - **Dockerfile Path:** `Dockerfile` (should auto-detect)
     - **Instance Type:** Free (or paid for better performance)

4. **Environment Variables** (if needed)
   - `FLASK_APP=app.py`
   - `DATABASE_URL=sqlite:////app/data/lab_tests.db`
   - `PYTHONUNBUFFERED=1`

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically:
     - Build your Docker image
     - Deploy it
     - Provide a URL (e.g., `https://lis-app.onrender.com`)

6. **Access Your App**
   - Your app will be available at: `https://your-app-name.onrender.com`
   - Free tier may spin down after inactivity (wakes on first request)

**Note:** Free tier has limitations (spins down after inactivity, slower cold starts)

---

### Option 2: Railway.app

**Why Railway?**
- Simple deployment
- GitHub integration
- Free tier with $5 credit monthly
- Good for Docker applications

#### Steps:

1. **Sign Up**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `Labtest-Management` repository

3. **Configure Deployment**
   - Railway auto-detects Dockerfile
   - Configure if needed:
     - **Port:** 5000
     - **Healthcheck:** `/health`

4. **Environment Variables** (optional)
   - Railway uses the same env vars from Dockerfile

5. **Deploy**
   - Railway builds and deploys automatically
   - Get your app URL (e.g., `https://lis-app.railway.app`)

---

### Option 3: Fly.io

**Why Fly.io?**
- Free tier with generous limits
- Global edge network
- Easy CLI deployment
- Good for Docker

#### Steps:

1. **Install Fly CLI**
   ```bash
   # Windows (PowerShell)
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   
   # Or download from: https://fly.io/docs/getting-started/installing-flyctl/
   ```

2. **Sign Up & Login**
   ```bash
   fly auth signup
   fly auth login
   ```

3. **Initialize Fly App**
   ```bash
   cd Labtestmanagement
   fly launch
   ```
   - Answer prompts:
     - App name: `lis-app` (or auto-generated)
     - Region: Choose closest
     - Deploy now? Yes

4. **Configure Port** (if needed)
   Create/update `fly.toml`:
   ```toml
   [[services]]
     internal_port = 5000
     protocol = "tcp"
   ```

5. **Deploy**
   ```bash
   fly deploy
   ```

6. **Access**
   - Your app: `https://lis-app.fly.dev`

---

## 3. Cloud Platforms

### AWS Options

#### Option A: AWS Elastic Beanstalk (Easiest AWS)

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize**
   ```bash
   eb init -p docker lis-app --region us-east-1
   ```

3. **Create Environment**
   ```bash
   eb create lis-env
   ```

4. **Deploy**
   ```bash
   eb deploy
   ```

5. **Access**
   ```bash
   eb open
   ```

#### Option B: AWS EC2 (Manual Setup)

1. **Launch EC2 Instance**
   - Choose Ubuntu Server
   - Configure security group (open port 5000)
   - Create key pair

2. **SSH into Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install Docker**
   ```bash
   sudo apt update
   sudo apt install docker.io -y
   sudo usermod -aG docker ubuntu
   ```

4. **Clone & Deploy**
   ```bash
   git clone https://github.com/ahmedshh/Labtest-Management.git
   cd Labtest-Management
   docker build -t lis:latest .
   docker run -d -p 5000:5000 --name lis-app lis:latest
   ```

5. **Configure Security Group**
   - Open port 5000 in AWS console
   - Access: `http://your-ec2-ip:5000`

#### Option C: AWS ECS (Container Service)

1. **Push Image to ECR** (Elastic Container Registry)
   ```bash
   aws ecr create-repository --repository-name lis-app
   aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.region.amazonaws.com
   docker tag lis:latest <account>.dkr.ecr.region.amazonaws.com/lis-app:latest
   docker push <account>.dkr.ecr.region.amazonaws.com/lis-app:latest
   ```

2. **Create ECS Cluster & Service** (via AWS Console or CLI)

---

### Google Cloud Platform

#### Using Cloud Run (Recommended)

1. **Install Google Cloud SDK**
   ```bash
   # Download from: https://cloud.google.com/sdk/docs/install
   ```

2. **Authenticate**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Build & Deploy**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/lis-app
   gcloud run deploy lis-app --image gcr.io/YOUR_PROJECT_ID/lis-app --platform managed --region us-central1 --allow-unauthenticated
   ```

4. **Access**
   - URL provided after deployment

---

### Microsoft Azure

#### Using Azure Container Instances

1. **Install Azure CLI**
   ```bash
   # Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
   ```

2. **Login & Create Resource Group**
   ```bash
   az login
   az group create --name lis-rg --location eastus
   ```

3. **Deploy Container**
   ```bash
   az container create \
     --resource-group lis-rg \
     --name lis-app \
     --image lis:latest \
     --dns-name-label lis-app \
     --ports 5000
   ```

---

## 4. Traditional VPS (DigitalOcean, Linode, etc.)

### DigitalOcean Droplet

1. **Create Droplet**
   - Choose Ubuntu 22.04
   - Select size (Basic $4/month minimum)
   - Add SSH key

2. **SSH into Droplet**
   ```bash
   ssh root@your-droplet-ip
   ```

3. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

4. **Clone & Deploy**
   ```bash
   git clone https://github.com/ahmedshh/Labtest-Management.git
   cd Labtest-Management
   docker build -t lis:latest .
   docker run -d -p 80:5000 --name lis-app lis:latest
   ```

5. **Set Up Nginx (Reverse Proxy - Optional)**
   ```bash
   apt install nginx -y
   # Configure nginx to proxy to port 5000
   ```

6. **Configure Firewall**
   ```bash
   ufw allow 80/tcp
   ufw allow 443/tcp
   ufw enable
   ```

---

## 5. Platform-as-a-Service (PaaS)

### Heroku

**Note:** Heroku removed free tier, but still a good option for paid deployment.

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create `heroku.yml`**
   ```yaml
   build:
     docker:
       web: Dockerfile
   run:
     web: python app.py
   ```

3. **Login & Deploy**
   ```bash
   heroku login
   heroku create lis-app
   heroku stack:set container
   git push heroku main
   ```

---

### DigitalOcean App Platform

1. **Go to DigitalOcean App Platform**
   - Navigate to: https://cloud.digitalocean.com/apps

2. **Create App from GitHub**
   - Connect GitHub
   - Select repository
   - Choose Docker
   - Configure:
     - **HTTP Port:** 5000
     - **Health Check:** `/health`

3. **Deploy**
   - DigitalOcean handles the rest
   - Free tier: $0/month for static sites, paid for Docker apps

---

## Recommended Deployment Options by Use Case

### 🎓 **For Learning/Demo (Free)**
**Best:** Render.com or Railway.app
- Easiest setup
- Free tier available
- Automatic GitHub deployments

### 💼 **For Production (Paid)**
**Best:** AWS ECS, Google Cloud Run, or DigitalOcean App Platform
- Scalable
- Reliable
- Good documentation

### 🏠 **For Personal Projects**
**Best:** Fly.io or Railway.app
- Good free tiers
- Simple deployment
- Good performance

### 🏢 **For Enterprise**
**Best:** AWS ECS, Azure Container Instances, or GCP Cloud Run
- Enterprise features
- Compliance support
- Advanced monitoring

---

## Post-Deployment Checklist

After deploying, ensure:

- [ ] Application is accessible via provided URL
- [ ] Health check endpoint works (`/health`)
- [ ] Database persistence is configured (volumes for SQLite)
- [ ] Environment variables are set correctly
- [ ] HTTPS is enabled (most platforms do this automatically)
- [ ] Monitoring/logging is configured (optional)
- [ ] Backup strategy is in place (for production)

---

## Environment Variables Reference

Common environment variables you might need:

```bash
FLASK_APP=app.py
DATABASE_URL=sqlite:////app/data/lab_tests.db
PYTHONUNBUFFERED=1
FLASK_ENV=production  # or development
PORT=5000  # Some platforms require this
```

---

## Troubleshooting

### Application Not Starting
- Check logs: `docker logs lis-app` or platform logs
- Verify port is correctly exposed
- Check environment variables

### Database Issues
- Ensure volume is mounted for data persistence
- Check database file permissions

### Build Failures
- Verify Dockerfile syntax
- Check platform Docker support
- Review build logs for errors

---

## Quick Comparison Table

| Platform | Free Tier | Setup Difficulty | Best For |
|----------|-----------|------------------|----------|
| Render.com | Yes (limited) | ⭐ Easy | Quick deployments |
| Railway.app | Yes ($5 credit) | ⭐ Easy | Docker apps |
| Fly.io | Yes | ⭐⭐ Medium | Global apps |
| AWS EC2 | No | ⭐⭐⭐ Hard | Full control |
| Google Cloud Run | Free tier | ⭐⭐ Medium | Serverless |
| DigitalOcean | No | ⭐⭐ Medium | VPS control |

---

## Next Steps After Deployment

1. **Set up CI/CD deployment** - Update GitHub Actions to auto-deploy
2. **Configure domain** - Point custom domain to your app
3. **Add monitoring** - Set up application monitoring
4. **Backup database** - Configure regular backups
5. **Enable HTTPS** - Most platforms do this automatically

---

**Need help with a specific platform?** Let me know which one you'd like to use, and I can provide more detailed steps!