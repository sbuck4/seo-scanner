# 🚀 SEO Scanner Pro - Deployment Guide

## Quick Start

### Option 1: Docker (Recommended)
```bash
# Clone or download your project
git clone <your-repo-url>
cd seo_scanner

# Build and run with Docker Compose
docker-compose up -d

# Access your app at http://localhost:8501
```

### Option 2: Direct Python
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
./start.sh
# or on Windows: start.bat
```

## 📋 Prerequisites

- **Docker & Docker Compose** (for containerized deployment)
- **Python 3.8+** (for direct deployment)
- **2GB RAM minimum** (4GB recommended for larger scans)
- **Internet access** (for website crawling)

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Key settings:
- `DEBUG=false` - Set to true for development
- `HOST=0.0.0.0` - Server bind address
- `PORT=8501` - Server port
- `LOG_LEVEL=INFO` - Logging verbosity
- `DEFAULT_MAX_PAGES=10` - Default crawl limit

### Docker Environment
The Docker setup automatically:
- ✅ Creates required directories (`logs/`, `reports/`)
- ✅ Sets up proper networking
- ✅ Includes health checks
- ✅ Handles restarts

## 🌐 Production Deployment

### Cloud Platforms

#### Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway deploy
```

#### Render
1. Connect your Git repository to Render
2. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

#### Streamlit Cloud
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy directly from your repository

#### DigitalOcean Droplet
```bash
# On your droplet
git clone <your-repo>
cd seo_scanner

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Deploy
docker-compose up -d
```

### Docker Hub Deployment
```bash
# Build and tag
docker build -t your-username/seo-scanner:latest .

# Push to Docker Hub
docker push your-username/seo-scanner:latest

# Deploy anywhere
docker run -p 8501:8501 your-username/seo-scanner:latest
```

## 📊 Monitoring & Health Checks

### Health Check Endpoint
- **URL**: `http://your-domain:8501/?health`
- **Response**: JSON with system status

### Log Files
- **Location**: `logs/seo-scanner-YYYYMMDD.log`
- **Rotation**: Daily
- **Levels**: ERROR, WARNING, INFO, DEBUG

### Docker Health Checks
```bash
# Check container health
docker-compose ps

# View logs
docker-compose logs seo-scanner

# Monitor resource usage
docker stats
```

## 🔒 Security Considerations

### Production Checklist
- [ ] Remove or secure debug endpoints
- [ ] Set strong environment variables
- [ ] Use HTTPS in production
- [ ] Configure firewall rules
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity

### Rate Limiting
The app includes basic rate limiting. For production:
- Use a reverse proxy (nginx)
- Implement API rate limiting
- Monitor crawl frequency

## 🚨 Troubleshooting

### Common Issues

#### "Module not found" errors
```bash
# Verify Python path
export PYTHONPATH=/app:$PYTHONPATH

# Or use Docker deployment (recommended)
```

#### Port already in use
```bash
# Change port in .env file
PORT=8502

# Or kill existing process
sudo lsof -ti:8501 | xargs kill -9
```

#### Crawling fails
- Check internet connectivity
- Verify website allows crawling (robots.txt)
- Increase timeout values in environment

#### Out of memory
- Reduce `DEFAULT_MAX_PAGES`
- Increase container memory limits
- Use a larger server instance

### Performance Tuning

#### For Large Sites
```env
# In .env file
DEFAULT_MAX_PAGES=50
REQUEST_TIMEOUT=60
MAX_CONCURRENT_REQUESTS=3
```

#### For High Traffic
- Use multiple container replicas
- Implement load balancing
- Consider caching strategies

## 📈 Scaling

### Horizontal Scaling
```yaml
# docker-compose.yml
services:
  seo-scanner:
    replicas: 3
    
  nginx:
    image: nginx
    # Load balancer config
```

### Vertical Scaling
```yaml
# Increase container resources
services:
  seo-scanner:
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2'
```

## 🔄 Updates & Maintenance

### Update Process
```bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker-compose down
docker-compose up -d --build

# Verify deployment
curl http://localhost:8501/?health
```

### Backup Strategy
- **Reports**: Automatically saved to `reports/` directory
- **Logs**: Retained in `logs/` directory
- **User Data**: Stored in session state (temporary)

## 🎯 Performance Optimization

### Production Optimizations
- ✅ Pinned dependency versions
- ✅ Multi-stage Docker builds
- ✅ Health checks enabled
- ✅ Proper logging configuration
- ✅ Error handling and recovery
- ✅ Resource monitoring

### Recommended Resources
- **CPU**: 2+ cores
- **RAM**: 4GB minimum
- **Storage**: 10GB for logs/reports
- **Network**: Stable internet connection

## 📞 Support

For deployment issues:
1. Check the logs: `docker-compose logs`
2. Verify health endpoint: `curl http://localhost:8501/?health`
3. Review environment variables
4. Check firewall/security groups

---

**🎉 Your SEO Scanner Pro is now production-ready!**

Access your deployed application and start analyzing websites with professional-grade SEO insights.