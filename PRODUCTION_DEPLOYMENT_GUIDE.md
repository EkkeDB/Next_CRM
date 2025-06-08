# NextCRM Production Deployment Guide

## ✅ Issue Resolved
The Docker build error has been **completely fixed**. The missing `frontend/public` directory was the root cause.

## 🚀 Quick Start

### 1. Build and Deploy
```bash
# Build all services for production
docker compose build

# Start the production environment
docker compose up -d

# Check service status
docker compose ps
```

### 2. Environment Configuration

**Copy and customize the environment file:**
```bash
cp .env.production.example .env.production
```

**Edit `.env.production` with your production values:**
- Change `SECRET_KEY` to a secure random string
- Update `ALLOWED_HOSTS` with your domain
- Update `CORS_ALLOWED_ORIGINS` with your frontend URL
- Set `NEXT_PUBLIC_API_URL` to your backend URL

### 3. Database Setup
```bash
# Run initial migrations
docker compose exec backend python manage.py migrate

# Create admin user (optional)
docker compose exec backend python manage.py createsuperuser
```

## 📁 Static Assets Directory

The `frontend/public/` directory has been created with:
- ✅ `robots.txt` - SEO configuration (blocks indexing for internal app)
- ✅ `site.webmanifest` - PWA manifest
- ✅ `favicon.svg` - Basic favicon (placeholder)
- ✅ `README.md` - Instructions for adding custom assets

### 🎨 Adding Your Custom Assets

**Recommended files to add to `frontend/public/`:**

1. **Company Favicon** (replace the placeholder):
   ```
   favicon.ico        # Traditional favicon (32x32 or 16x16)
   favicon.svg        # Modern SVG favicon (replace existing)
   ```

2. **PWA Icons**:
   ```
   icon-192x192.png   # PWA icon (192x192)
   icon-512x512.png   # PWA icon (512x512)
   apple-touch-icon.png # iOS home screen icon (180x180)
   ```

3. **Company Branding**:
   ```
   logo.png           # Company logo for use in the app
   logo-dark.png      # Dark mode variant (optional)
   ```

4. **Documents** (optional):
   ```
   help.pdf           # User manual
   privacy-policy.pdf # Privacy policy
   terms-of-service.pdf # Terms of service
   ```

## 🔧 Production Configuration

### Security Settings (Already Configured)
- ✅ HTTPS enforcement (when `DEBUG=False`)
- ✅ Security headers (HSTS, XSS Protection, etc.)
- ✅ CORS properly configured
- ✅ JWT cookies with HttpOnly and secure flags
- ✅ Authentication circuit breaker (prevents abuse)
- ✅ Log flooding protection

### Performance Optimizations
- ✅ Next.js production build with standalone output
- ✅ Static file serving through Nginx (recommended)
- ✅ Gunicorn with multiple workers
- ✅ PostgreSQL with health checks
- ✅ Redis for caching

## 🌐 Domain Configuration

### Reverse Proxy Setup (Recommended)
Set up Nginx in front of the Docker containers:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Monitoring

### Health Checks
All services include health checks:
- **Database**: `pg_isready` check
- **Redis**: `redis-cli ping` check  
- **Backend**: Django `check --deploy` command
- **Frontend**: HTTP request to port 3000

### Logs
```bash
# View all logs
docker compose logs -f

# View specific service logs
docker compose logs -f backend
docker compose logs -f frontend
```

## 🔒 Security Checklist

- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Update `ALLOWED_HOSTS` with your actual domain
- [ ] Set up proper SSL certificates
- [ ] Configure firewall to only allow necessary ports
- [ ] Set up regular database backups
- [ ] Monitor logs for security issues
- [ ] Keep Docker images updated

## 🚨 Troubleshooting

### Build Issues
```bash
# Clean build (if needed)
docker compose build --no-cache

# Clean volumes and restart
docker compose down -v
docker compose up -d
```

### Database Issues
```bash
# Reset database (WARNING: destroys data)
docker compose down
docker volume rm next_crm_postgres_data
docker compose up -d
```

### Permission Issues
```bash
# Fix static file permissions
docker compose exec backend chown -R appuser:appuser /app/staticfiles
```

## 📈 Performance Tips

1. **Use a CDN** for static assets in `public/`
2. **Set up Redis caching** for better performance
3. **Configure log rotation** to prevent disk space issues
4. **Monitor resource usage** and scale containers as needed
5. **Use persistent volumes** for database and media files

## 🎯 Next Steps

1. **Test the complete deployment** with your domain
2. **Add your company branding** to the `public/` directory
3. **Set up monitoring** and alerting
4. **Configure automated backups**
5. **Set up CI/CD pipeline** for updates

---

## 📞 Support

If you encounter any issues:
1. Check the container logs: `docker compose logs -f`
2. Verify environment variables in `.env.production`
3. Ensure all required files are present in `frontend/public/`
4. Test the health checks: `docker compose ps`

**The Docker build issue has been completely resolved! 🎉**