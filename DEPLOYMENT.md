# Deployment Guide

## Local Development

### Backend
```bash
# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python create_data.py

# Run server
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Production Deployment

### Option 1: Railway (Recommended for Quick Deploy)

#### Backend
1. Create account at [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add environment variables:
   ```
   DEBUG=False
   SECRET_KEY=<generate-strong-key>
   ALLOWED_HOSTS=<your-railway-domain>
   DATABASE_URL=<railway-postgres-url>
   ```
5. Railway will auto-detect Django and deploy

#### Frontend
1. Create new Railway service
2. Select your repository
3. Set root directory to `frontend`
4. Add environment variable:
   ```
   REACT_APP_API_URL=<your-backend-url>
   ```

### Option 2: Vercel (Frontend) + Railway (Backend)

#### Backend on Railway
Same as above

#### Frontend on Vercel
1. Install Vercel CLI: `npm i -g vercel`
2. Navigate to frontend: `cd frontend`
3. Deploy: `vercel --prod`
4. Set environment variable in Vercel dashboard:
   ```
   REACT_APP_API_URL=<your-backend-url>
   ```

### Option 3: AWS (Full Control)

#### Backend on EC2
```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Clone repository
git clone <your-repo-url>
cd playto-community-feed

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn

# Setup environment variables
cp .env.example .env
nano .env  # Edit with production values

# Run migrations
python manage.py migrate
python manage.py collectstatic

# Setup Gunicorn service
sudo nano /etc/systemd/system/gunicorn.service
```

Gunicorn service file:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/playto-community-feed
ExecStart=/home/ubuntu/playto-community-feed/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/ubuntu/playto-community-feed/gunicorn.sock \
          backend.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Start Gunicorn
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Configure Nginx
sudo nano /etc/nginx/sites-available/playto
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/playto-community-feed;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/playto-community-feed/gunicorn.sock;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/playto /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

#### Frontend on S3 + CloudFront
```bash
cd frontend

# Build production bundle
npm run build

# Upload to S3
aws s3 sync build/ s3://your-bucket-name --delete

# Create CloudFront distribution pointing to S3 bucket
# Configure custom domain and SSL certificate
```

### Database Migration to PostgreSQL

1. Install PostgreSQL:
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql
```

2. Create database:
```bash
sudo -u postgres psql
CREATE DATABASE playto_feed;
CREATE USER playto_user WITH PASSWORD 'your_password';
ALTER ROLE playto_user SET client_encoding TO 'utf8';
ALTER ROLE playto_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE playto_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE playto_feed TO playto_user;
\q
```

3. Update settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'playto_feed'),
        'USER': os.getenv('DB_USER', 'playto_user'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

4. Run migrations:
```bash
python manage.py migrate
```

## Environment Variables

### Required for Production
- `DEBUG=False`
- `SECRET_KEY=<strong-random-key>`
- `ALLOWED_HOSTS=<your-domain>`
- `DATABASE_URL=<postgres-connection-string>`
- `CORS_ALLOWED_ORIGINS=<frontend-url>`

### Generate Secret Key
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Use HTTPS (SSL certificate)
- [ ] Set up CORS correctly
- [ ] Use environment variables for secrets
- [ ] Enable Django security middleware
- [ ] Set up database backups
- [ ] Configure rate limiting
- [ ] Set up monitoring and logging

## Monitoring

### Sentry (Error Tracking)
```bash
pip install sentry-sdk
```

Add to settings.py:
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

### Performance Monitoring
- Use Django Debug Toolbar in development
- Set up APM (Application Performance Monitoring)
- Monitor database query performance
- Track API response times

## Scaling Considerations

### Database
- Add read replicas for heavy read workloads
- Implement connection pooling (pgBouncer)
- Add database indexes for frequently queried fields
- Consider partitioning for large tables

### Caching
- Add Redis for caching
- Cache leaderboard results (5-minute TTL)
- Cache user karma calculations
- Use Django's cache framework

### Load Balancing
- Use multiple application servers
- Set up load balancer (AWS ALB, Nginx)
- Implement session management (Redis)

### CDN
- Serve static files through CDN
- Cache API responses at edge locations
- Use CloudFront or Cloudflare

## Backup Strategy

### Database Backups
```bash
# Automated daily backups
pg_dump playto_feed > backup_$(date +%Y%m%d).sql

# Restore from backup
psql playto_feed < backup_20260204.sql
```

### Media Files
- Store user uploads in S3
- Enable versioning
- Set up lifecycle policies

## Troubleshooting

### Common Issues

1. **Static files not loading**
   ```bash
   python manage.py collectstatic
   ```

2. **Database connection errors**
   - Check DATABASE_URL format
   - Verify database credentials
   - Ensure PostgreSQL is running

3. **CORS errors**
   - Add frontend URL to CORS_ALLOWED_ORIGINS
   - Check CORS middleware order

4. **502 Bad Gateway**
   - Check Gunicorn is running
   - Verify Nginx configuration
   - Check application logs

### Logs
```bash
# Django logs
tail -f /var/log/django/error.log

# Gunicorn logs
sudo journalctl -u gunicorn -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
```

## Support

For issues or questions:
- Check EXPLAINER.md for technical details
- Review test cases in feed/tests.py
- Open an issue on GitHub
