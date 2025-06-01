#!/bin/bash

# Deployment script for Quickfiss Django application on AlmaLinux
# Run as: chmod +x deploy.sh && ./deploy.sh

set -e

echo "🚀 Starting Quickfiss deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if container-selinux is installed (required for Docker on AlmaLinux)
if ! rpm -q container-selinux &> /dev/null; then
    print_status "Installing container-selinux for SELinux compatibility..."
    sudo dnf install -y container-selinux
fi

# Check if Docker Compose V2 is installed
if ! docker compose version &> /dev/null; then
    print_error "Docker Compose V2 is not installed. Installing..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
fi

# Add current user to docker group (optional, for non-root Docker access)
if ! groups $USER | grep -q docker; then
    print_status "Adding $USER to docker group..."
    sudo usermod -aG docker $USER
    print_warning "You may need to log out and back in for Docker group changes to take effect."
fi

# Stop and remove existing containers
print_status "Stopping existing containers..."
sudo docker compose down --remove-orphans

# Clean up old images (optional)
print_status "Cleaning up old Docker images..."
sudo docker system prune -f

# Build and start services
print_status "Building and starting services..."
sudo docker compose up -d --build

# Wait for database to be ready
print_status "Waiting for database to be ready..."
sleep 10

# Run database migrations
print_status "Running database migrations..."
sudo docker compose exec -T web python manage.py makemigrations
sudo docker compose exec -T web python manage.py migrate

# Collect static files
print_status "Collecting static files..."
sudo docker compose exec -T web python manage.py collectstatic --noinput

# Create superuser (optional)
print_warning "Do you want to create a superuser? (y/n)"
read -r create_superuser
if [[ $create_superuser == "y" || $create_superuser == "Y" ]]; then
    sudo docker compose exec web python manage.py createsuperuser
fi




# Reload Nginx to use SSL
print_status "Reloading Nginx with SSL configuration..."
sudo docker compose exec nginx nginx -s reload

print_status "✅ Deployment completed successfully!"
print_status "Your application should be accessible at: https://quickfiss.com"

echo ""
print_warning "Don't forget to:"
echo "1. Update your environment variables in docker-compose.yml"
echo "2. Change default passwords"
echo "3. Update the email address in the SSL certificate command (your-email@example.com)"
echo "4. Set up regular backups for your database"
echo "5. Configure firewalld if enabled (e.g., allow ports 80 and 443)"

# Open firewall ports for HTTP/HTTPS (if firewalld is active)
if systemctl is-active --quiet firewalld; then
    print_status "Configuring firewalld to allow HTTP and HTTPS..."
    sudo firewall-cmd --permanent --add-service=http
    sudo firewall-cmd --permanent --add-service=https
    sudo firewall-cmd --reload
fi

# Show running containers
print_status "Currently running containers:"
sudo docker compose ps