#!/bin/bash

# NextCRM Dev Container Setup Script
echo "🚀 Setting up NextCRM Development Environment..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
until pg_isready -h postgres -p 5432 -U nextcrm; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 1
done
echo "✅ PostgreSQL is ready!"

# Backend Setup
echo "🐍 Setting up Python backend..."
cd /workspace/backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install development dependencies
pip install \
    black \
    flake8 \
    isort \
    pylint \
    pytest \
    pytest-django \
    django-extensions \
    ipython

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --settings=core.settings.development

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
python manage.py shell --settings=core.settings.development << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@nextcrm.com', 'admin123')
    print("Superuser 'admin' created with password 'admin123'")
else:
    print("Superuser 'admin' already exists")
EOF

# Frontend Setup
echo "📦 Setting up Node.js frontend..."
cd /workspace/frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Creating frontend .env.local..."
    cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_APP_URL=http://localhost:3001
NODE_ENV=development
EOF
fi

# Backend environment setup
echo "🔧 Setting up backend environment..."
cd /workspace/backend

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating backend .env..."
    cat > .env << EOF
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=postgresql://nextcrm:nextcrm123@postgres:5432/nextcrm_dev
REDIS_URL=redis://redis:6379/0
CORS_ALLOW_ALL_ORIGINS=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,backend,nextcrm_backend_dev

# Email settings (using MailHog)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=mailhog
EMAIL_PORT=1025
EMAIL_USE_TLS=False
EMAIL_USE_SSL=False
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Development settings
DJANGO_SETTINGS_MODULE=core.settings.development
EOF
fi

# Set up git hooks
echo "🔗 Setting up Git hooks..."
cd /workspace

# Install pre-commit if available
if command -v pre-commit &> /dev/null; then
    pre-commit install
fi

# Create useful aliases
echo "⚡ Setting up shell aliases..."
cat >> /home/vscode/.bashrc << 'EOF'

# NextCRM Development Aliases
alias backend="cd /workspace/backend && source venv/bin/activate"
alias frontend="cd /workspace/frontend"
alias runserver="cd /workspace/backend && source venv/bin/activate && python manage.py runserver 0.0.0.0:8001 --settings=core.settings.development"
alias nextdev="cd /workspace/frontend && npm run dev -- --port 3001"
alias migrate="cd /workspace/backend && source venv/bin/activate && python manage.py migrate --settings=core.settings.development"
alias makemigrations="cd /workspace/backend && source venv/bin/activate && python manage.py makemigrations --settings=core.settings.development"
alias shell="cd /workspace/backend && source venv/bin/activate && python manage.py shell --settings=core.settings.development"
alias test-backend="cd /workspace/backend && source venv/bin/activate && python manage.py test --settings=core.settings.development"
alias test-frontend="cd /workspace/frontend && npm run test"
alias lint-backend="cd /workspace/backend && source venv/bin/activate && flake8 . && black --check . && isort --check-only ."
alias lint-frontend="cd /workspace/frontend && npm run lint"
alias format-backend="cd /workspace/backend && source venv/bin/activate && black . && isort ."
alias format-frontend="cd /workspace/frontend && npm run format"

# Quick development commands
alias start-all="runserver & nextdev"
alias logs="docker-compose -f .devcontainer/docker-compose.yml logs -f"
alias rebuild="docker-compose -f .devcontainer/docker-compose.yml up --build -d"

echo "🎉 NextCRM Development Environment Ready!"
echo ""
echo "Quick Start Commands:"
echo "  backend      - Navigate to backend & activate venv"
echo "  frontend     - Navigate to frontend"
echo "  runserver    - Start Django development server"
echo "  nextdev      - Start Next.js development server"
echo "  migrate      - Run Django migrations"
echo "  shell        - Open Django shell"
echo ""
echo "Services:"
echo "  Frontend:    http://localhost:3001"
echo "  Backend:     http://localhost:8001"
echo "  Admin:       http://localhost:8001/admin (admin/admin123)"
echo "  MailHog:     http://localhost:8025"
echo "  PostgreSQL:  localhost:5432 (nextcrm/nextcrm123)"
echo ""
EOF

echo "✅ NextCRM Development Environment Setup Complete!"
echo ""
echo "🌟 Your development environment is ready!"
echo ""
echo "🔗 Quick Access:"
echo "   Frontend: http://localhost:3001"
echo "   Backend:  http://localhost:8001"
echo "   Admin:    http://localhost:8001/admin (admin/admin123)"
echo "   MailHog:  http://localhost:8025"
echo ""
echo "🚀 To start development:"
echo "   1. Run 'runserver' to start the Django backend"
echo "   2. Run 'nextdev' to start the Next.js frontend"
echo "   3. Or use VS Code task 'Start Both Servers'"
echo ""