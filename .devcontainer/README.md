# NextCRM Dev Container

This directory contains the VS Code Dev Container configuration for the NextCRM project, providing a consistent, isolated development environment.

## 🚀 Quick Start

1. **Open in Dev Container**:
   - Install the "Dev Containers" extension in VS Code
   - Open the project folder in VS Code
   - When prompted, click "Reopen in Container"
   - Or use Command Palette: `Dev Containers: Reopen in Container`

2. **Wait for Setup**:
   - The container will build and run the setup script automatically
   - This includes installing dependencies, setting up the database, and creating a superuser

3. **Start Development**:
   ```bash
   # Start Django backend
   runserver
   
   # Start Next.js frontend (in another terminal)
   nextdev
   
   # Or use VS Code task: "Start Both Servers"
   ```

## 🔧 What's Included

### **Services**
- **Workspace**: Main development container with Python 3.11 and Node.js 18
- **PostgreSQL**: Database server (nextcrm_dev/nextcrm_test databases)
- **Redis**: Caching and session storage
- **MailHog**: Email testing server

### **Development Tools**
- **Python**: Black, Flake8, isort, Pylint, pytest
- **Node.js**: TypeScript, ESLint, Prettier, Next.js CLI
- **VS Code Extensions**: Python, Django, TypeScript, React, Tailwind CSS, Docker, GitLens
- **Database Tools**: PostgreSQL client, Redis tools
- **Git Tools**: GitHub CLI, GitLens

### **Ports Forwarded**
- `3001` - Frontend (Next.js)
- `8001` - Backend (Django)
- `5432` - PostgreSQL
- `6379` - Redis
- `8025` - MailHog Web UI

## 📁 File Structure

```
.devcontainer/
├── devcontainer.json    # Dev container configuration
├── docker-compose.yml   # Services definition
├── Dockerfile          # Development container image
├── setup.sh            # Automatic setup script
├── init-db.sql         # Database initialization
└── README.md           # This file
```

## 🛠️ Configuration Details

### **Python Environment**
- Virtual environment in `backend/venv/`
- Django development settings
- Pre-configured superuser: `admin` / `admin123`
- Database migrations run automatically

### **Node.js Environment**
- All dependencies installed
- Development server on port 3001
- TypeScript configuration
- ESLint and Prettier setup

### **Database Configuration**
- PostgreSQL 15 with two databases:
  - `nextcrm_dev` - Development database
  - `nextcrm_test` - Testing database
- User: `nextcrm` / Password: `nextcrm123`

### **VS Code Settings**
- Python formatter: Black
- TypeScript formatter: Prettier
- Auto-format on save
- Proper file associations
- Debugging configurations

## 🚀 Development Workflow

### **Starting Services**
```bash
# Backend only
runserver

# Frontend only  
nextdev

# Both services (VS Code task)
Ctrl+Shift+P → "Tasks: Run Task" → "Start Both Servers"
```

### **Database Operations**
```bash
# Run migrations
migrate

# Create migrations
makemigrations

# Django shell
shell

# Create superuser
cd backend && python manage.py createsuperuser --settings=core.settings.development
```

### **Testing**
```bash
# Backend tests
test-backend

# Frontend tests
test-frontend

# Linting
lint-backend
lint-frontend

# Formatting
format-backend
format-frontend
```

### **Debugging**
- Use VS Code's built-in debugger
- Configurations available for:
  - Django backend debugging
  - Next.js frontend debugging
  - Django tests
  - Django shell

## 🔧 Customization

### **Adding Python Packages**
1. Add to `backend/requirements.txt`
2. Rebuild container or run `pip install -r requirements.txt`

### **Adding Node.js Packages**
1. Use `npm install <package>` in the frontend directory
2. Packages persist in the container volume

### **Environment Variables**
- Backend: `.env` file in `backend/` directory
- Frontend: `.env.local` file in `frontend/` directory

### **VS Code Extensions**
- Add extensions to `devcontainer.json` in the `customizations.vscode.extensions` array
- Extensions are installed automatically on container build

## 🐛 Troubleshooting

### **Container Won't Start**
```bash
# Rebuild container
docker-compose -f .devcontainer/docker-compose.yml down
docker-compose -f .devcontainer/docker-compose.yml up --build
```

### **Database Connection Issues**
```bash
# Check PostgreSQL is running
docker-compose -f .devcontainer/docker-compose.yml ps

# View PostgreSQL logs
docker-compose -f .devcontainer/docker-compose.yml logs postgres
```

### **Port Conflicts**
- Change ports in `docker-compose.yml` if needed
- Update `devcontainer.json` forwardPorts accordingly

### **Permission Issues**
```bash
# Fix file permissions
sudo chown -R vscode:vscode /workspace
```

## 📊 Services Access

| Service | URL | Credentials |
|---------|-----|-------------|
| **Frontend** | http://localhost:3001 | - |
| **Backend API** | http://localhost:8001 | - |
| **Django Admin** | http://localhost:8001/admin | admin / admin123 |
| **MailHog UI** | http://localhost:8025 | - |
| **PostgreSQL** | localhost:5432 | nextcrm / nextcrm123 |
| **Redis** | localhost:6379 | - |

## 🎯 Benefits

### **Consistency**
- Same environment for all developers
- Reproducible builds and testing
- No "works on my machine" issues

### **Isolation**
- No conflicts with host system
- Clean environment for each project
- Easy to reset and rebuild

### **Productivity**
- Pre-configured tools and extensions
- Automatic setup and initialization
- Integrated debugging and testing
- Quick access to all services

### **Collaboration**
- Shared development environment
- Consistent code formatting
- Standardized tooling
- Easy onboarding for new developers