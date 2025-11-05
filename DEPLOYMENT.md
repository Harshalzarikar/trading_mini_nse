# 🚀 Deployment Guide - NSE Trading Platform

This guide covers deploying your NSE Trading Platform to production.

## Prerequisites

- Server with Python 3.8+
- Domain name (optional but recommended)
- SSL certificate for HTTPS/WSS
- PostgreSQL database (recommended for production)
- Redis (for channel layers in production)

## Production Configuration

### 1. Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/nse_trading

# Redis (for WebSocket channel layers)
REDIS_URL=redis://localhost:6379/0

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 2. Update settings.py

Add to `nse_project/settings.py`:

```python
import os
from decouple import config

# Security
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Database
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

# Channel Layers (Redis for production)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [config('REDIS_URL', default='redis://localhost:6379/0')],
        },
    },
}

# Security Settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

### 3. Install Production Dependencies

Update `requirements.txt`:

```txt
# Add these for production
dj-database-url==2.2.0
channels-redis==4.2.0
redis==5.2.1
gunicorn==23.0.0
whitenoise==6.8.2
```

Install:
```bash
pip install -r requirements.txt
```

## Deployment Options

### Option 1: Traditional VPS (DigitalOcean, AWS EC2, etc.)

#### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx postgresql redis-server -y

# Create app directory
sudo mkdir -p /var/www/nse-trading
cd /var/www/nse-trading
```

#### 2. Clone and Setup

```bash
# Clone repository
git clone <your-repo-url> .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate
python manage.py collectstatic --noinput
```

#### 3. Configure Gunicorn

Create `/etc/systemd/system/nse-trading.service`:

```ini
[Unit]
Description=NSE Trading Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/nse-trading/nse_project
Environment="PATH=/var/www/nse-trading/venv/bin"
ExecStart=/var/www/nse-trading/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/nse-trading/gunicorn.sock \
    nse_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### 4. Configure Daphne (for WebSocket)

Create `/etc/systemd/system/nse-trading-daphne.service`:

```ini
[Unit]
Description=NSE Trading Daphne Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/nse-trading/nse_project
Environment="PATH=/var/www/nse-trading/venv/bin"
ExecStart=/var/www/nse-trading/venv/bin/daphne \
    -b 0.0.0.0 \
    -p 8001 \
    nse_project.asgi:application

[Install]
WantedBy=multi-user.target
```

#### 5. Configure Nginx

Create `/etc/nginx/sites-available/nse-trading`:

```nginx
upstream django {
    server unix:/var/www/nse-trading/gunicorn.sock;
}

upstream daphne {
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    client_max_body_size 10M;

    location /static/ {
        alias /var/www/nse-trading/nse_project/staticfiles/;
    }

    location /media/ {
        alias /var/www/nse-trading/nse_project/media/;
    }

    location /ws/ {
        proxy_pass http://daphne;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/nse-trading /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. Start Services

```bash
sudo systemctl start nse-trading
sudo systemctl start nse-trading-daphne
sudo systemctl enable nse-trading
sudo systemctl enable nse-trading-daphne
```

#### 7. Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Option 2: Docker Deployment

#### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY nse_project/ ./nse_project/

WORKDIR /app/nse_project

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "nse_project.asgi:application"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: nse_trading
      POSTGRES_USER: nse_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

  web:
    build: .
    command: daphne -b 0.0.0.0 -p 8000 nse_project.asgi:application
    volumes:
      - ./nse_project:/app/nse_project
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://nse_user:secure_password@db:5432/nse_trading
      - REDIS_URL=redis://redis:6379/0
      - DEBUG=False

volumes:
  postgres_data:
```

#### 3. Deploy

```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Option 3: Heroku Deployment

#### 1. Create Procfile

```
web: daphne nse_project.asgi:application --port $PORT --bind 0.0.0.0
release: python nse_project/manage.py migrate
```

#### 2. Create runtime.txt

```
python-3.11.0
```

#### 3. Deploy

```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
heroku addons:create heroku-redis:mini
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
git push heroku main
heroku run python nse_project/manage.py createsuperuser
```

## Post-Deployment Checklist

- [ ] Verify all environment variables are set
- [ ] Test database connection
- [ ] Test Redis connection
- [ ] Verify static files are served correctly
- [ ] Test WebSocket connection (wss://)
- [ ] Test buy/sell functionality
- [ ] Verify real-time updates work
- [ ] Check SSL certificate is valid
- [ ] Setup monitoring and logging
- [ ] Configure backups
- [ ] Setup error tracking (Sentry)
- [ ] Test on mobile devices
- [ ] Verify email notifications (if implemented)

## Monitoring

### Setup Logging

Add to `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/nse-trading/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Monitor Services

```bash
# Check service status
sudo systemctl status nse-trading
sudo systemctl status nse-trading-daphne

# View logs
sudo journalctl -u nse-trading -f
sudo journalctl -u nse-trading-daphne -f
```

## Backup Strategy

### Database Backup

```bash
# Backup
pg_dump -U username nse_trading > backup_$(date +%Y%m%d).sql

# Restore
psql -U username nse_trading < backup_20240101.sql
```

### Automated Backups

Create cron job:
```bash
0 2 * * * /usr/bin/pg_dump -U username nse_trading > /backups/nse_$(date +\%Y\%m\%d).sql
```

## Performance Optimization

1. **Enable caching**
   - Use Redis for caching
   - Cache stock prices for 1-2 minutes

2. **Database optimization**
   - Add indexes on frequently queried fields
   - Use connection pooling

3. **CDN for static files**
   - Use CloudFlare or AWS CloudFront

4. **Load balancing**
   - Use multiple Gunicorn workers
   - Setup load balancer for high traffic

## Security Best Practices

- Keep SECRET_KEY secure and unique
- Use strong database passwords
- Enable HTTPS/WSS only
- Regular security updates
- Implement rate limiting
- Use CORS headers properly
- Regular security audits
- Monitor for suspicious activity

## Troubleshooting

### WebSocket not working
- Check Daphne is running
- Verify Nginx WebSocket configuration
- Check firewall rules
- Verify SSL certificate for WSS

### Database connection errors
- Check DATABASE_URL
- Verify PostgreSQL is running
- Check user permissions

### Static files not loading
- Run `collectstatic`
- Check Nginx static file configuration
- Verify file permissions

---

**Good luck with your deployment! 🚀**
