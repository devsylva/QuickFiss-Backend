#!/bin/bash

# Deployment script for Quickfiss Django application on AlmaLinux

set -e

echo "🚀 Starting Quickfiss deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on AlmaLinux
if ! grep -qi "almalinux" /etc/os-release; then
    print_error "This script is designed for AlmaLinux. Exiting."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Installing Docker..."
    sudo dnf install -y dnf-utils
    sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    sudo dnf install -y docker-ce docker-ce-cli containerd.io
    sudo systemctl start docker
    sudo systemctl enable docker
fi

# Check if container-selinux is installed
if ! rpm -q container-selinux &> /dev/null; then
    print_status "Installing container-selinux for SELinux compatibility..."
    sudo dnf install -y container-selinux
fi

# Check if Docker Compose plugin is installed
if ! docker compose version &> /dev/null; then
    print_error "Docker Compose plugin is not installed. Installing..."
    sudo dnf install -y docker-compose-plugin
fi

# Add current user to docker group
if ! groups $USER | grep -q docker; then
    print_status "Adding $USER to docker group..."
    sudo usermod -aG docker $USER
    print_warning "Log out and back in for Docker group changes to take effect."
fi

# Create logs directory
print_status "Creating logs directory..."
mkdir -p logs
chmod 755 logs

# Stop and remove existing containers
print_status "Stopping existing containers..."
docker compose down --remove-orphans

# Clean up old images
print_status "Cleaning up old Docker images..."
docker system prune -f

# Build and start services
print_status "Building and starting services..."
docker compose up -d --build

# Wait for database to be ready
print_status "Waiting for database to be ready..."
sleep 10

# Run database migrations
print_status "Running database migrations..."
docker compose exec -T web python manage.py makemigrations
docker compose exec -T web python manage.py migrate

# Collect static files
print_status "Collecting static files..."
docker compose exec -T web python manage.py collectstatic --noinput

# Create superuser (non-interactive for automation)
if [ ! -f .superuser_created ]; then
    print_status "Creating superuser..."
    docker compose exec -T web python manage.py createsuperuser --noinput --email admin@quickfiss.com || true
    touch .superuser_created
fi

# Reload Nginx
print_status "Reloading Nginx..."
docker compose exec nginx nginx -s reload

print_status "✅ Deployment completed successfully!"
print_status "Your application should be accessible at: https://quickfiss.com"

print_warning "Don't forget to:"
echo "1. Update your environment variables in .env"
echo "2. Change default passwords"
echo "3. Set up SSL with Certbot"
echo "4. Set up regular backups for your database"
echo "5. Configure firewalld (allow ports 80, 443)"

# Show running containers
print_status "Currently running containers:"
docker compose ps