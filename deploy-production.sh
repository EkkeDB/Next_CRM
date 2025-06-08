#!/bin/bash

# NextCRM Production Deployment Script
# This script helps deploy NextCRM in production environment

set -e  # Exit on any error

echo "🚀 NextCRM Production Deployment Script"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker and Docker Compose are installed
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Check if frontend/public directory exists
check_public_directory() {
    print_status "Checking frontend public directory..."
    
    if [ ! -d "frontend/public" ]; then
        print_error "frontend/public directory not found!"
        print_error "This directory should have been created automatically."
        print_error "Please check the deployment guide."
        exit 1
    fi
    
    print_success "frontend/public directory exists"
}

# Build the Docker images
build_images() {
    print_status "Building Docker images..."
    
    if docker compose build; then
        print_success "Docker images built successfully"
    else
        print_error "Failed to build Docker images"
        exit 1
    fi
}

# Start the services
start_services() {
    print_status "Starting production services..."
    
    if docker compose up -d; then
        print_success "Services started successfully"
    else
        print_error "Failed to start services"
        exit 1
    fi
}

# Check service health
check_health() {
    print_status "Checking service health..."
    
    # Wait a bit for services to start
    sleep 10
    
    # Check if containers are running
    if docker compose ps --filter "status=running" | grep -q "nextcrm"; then
        print_success "Services are running"
    else
        print_warning "Some services may not be running properly"
        docker compose ps
    fi
}

# Run database migrations
run_migrations() {
    print_status "Running database migrations..."
    
    if docker compose exec -T backend python manage.py migrate; then
        print_success "Database migrations completed"
    else
        print_warning "Database migrations failed or already up to date"
    fi
}

# Show deployment status
show_status() {
    echo
    print_status "Deployment Status:"
    echo "=================="
    
    # Show running containers
    docker compose ps
    
    echo
    print_status "Service URLs:"
    echo "Frontend: http://localhost:3000"
    echo "Backend API: http://localhost:8000"
    echo "Database: localhost:5432"
    echo "Redis: localhost:6379"
    
    echo
    print_status "Useful Commands:"
    echo "View logs: docker compose logs -f"
    echo "Stop services: docker compose down"
    echo "Restart services: docker compose restart"
    echo "Enter backend shell: docker compose exec backend bash"
    echo "Enter frontend shell: docker compose exec frontend sh"
}

# Main deployment function
main() {
    print_status "Starting NextCRM production deployment..."
    echo
    
    check_prerequisites
    check_public_directory
    build_images
    start_services
    check_health
    run_migrations
    
    echo
    print_success "🎉 NextCRM deployment completed successfully!"
    echo
    
    show_status
    
    echo
    print_warning "Important Notes:"
    echo "1. Update your .env.production file with production values"
    echo "2. Add your company assets to frontend/public/ directory"
    echo "3. Set up SSL/TLS certificates for production"
    echo "4. Configure your domain and reverse proxy"
    echo "5. Set up regular database backups"
    echo
    print_status "See PRODUCTION_DEPLOYMENT_GUIDE.md for detailed instructions"
}

# Handle script arguments
case "${1:-}" in
    "build")
        check_prerequisites
        check_public_directory
        build_images
        ;;
    "start")
        start_services
        check_health
        ;;
    "stop")
        print_status "Stopping services..."
        docker compose down
        print_success "Services stopped"
        ;;
    "restart")
        print_status "Restarting services..."
        docker compose restart
        print_success "Services restarted"
        ;;
    "logs")
        docker compose logs -f
        ;;
    "status")
        show_status
        ;;
    "clean")
        print_warning "This will remove all containers, images, and volumes!"
        read -p "Are you sure? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker compose down -v --rmi all
            print_success "Cleaned up successfully"
        else
            print_status "Clean up cancelled"
        fi
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [COMMAND]"
        echo
        echo "Commands:"
        echo "  (no command)  Full deployment (default)"
        echo "  build         Build Docker images only"
        echo "  start         Start services only"
        echo "  stop          Stop all services"
        echo "  restart       Restart all services"
        echo "  logs          View service logs"
        echo "  status        Show deployment status"
        echo "  clean         Clean up all containers and volumes"
        echo "  help          Show this help message"
        ;;
    "")
        main
        ;;
    *)
        print_error "Unknown command: $1"
        print_status "Use '$0 help' for usage information"
        exit 1
        ;;
esac