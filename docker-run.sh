#!/bin/bash

# Docker run script for python-server-error

set -e

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

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to build the Docker image
build_image() {
    print_status "Building Docker image..."
    docker build -t python-server-error .
    print_status "Docker image built successfully!"
}

# Function to run the container
run_container() {
    print_status "Starting container..."
    docker run -d \
        --name python-server-error \
        -p 5000:5000 \
        -e PORT=5000 \
        -e FLASK_ENV=production \
        -e LOG_LEVEL=INFO \
        -v $(pwd)/logs:/app/logs \
        --restart unless-stopped \
        python-server-error
    
    print_status "Container started successfully!"
    print_status "Server is running at http://localhost:5000"
    print_status "Health check: http://localhost:5000/health"
    print_status "Logs are available in ./logs/ directory"
}

# Function to stop the container
stop_container() {
    print_status "Stopping container..."
    docker stop python-server-error 2>/dev/null || true
    docker rm python-server-error 2>/dev/null || true
    print_status "Container stopped and removed!"
}

# Function to show logs
show_logs() {
    print_status "Showing container logs..."
    docker logs -f python-server-error
}

# Function to show container status
show_status() {
    print_status "Container status:"
    docker ps -a --filter name=python-server-error
}

# Function to run with docker-compose
run_compose() {
    print_status "Starting with docker-compose..."
    docker-compose up -d
    print_status "Services started successfully!"
    print_status "Server is running at http://localhost:5000"
    print_status "Logs are available in ./logs/ directory"
}

# Function to run with custom log level
run_with_log_level() {
    local log_level=${1:-INFO}
    print_status "Starting container with LOG_LEVEL=$log_level..."
    docker run -d \
        --name python-server-error \
        -p 5000:5000 \
        -e PORT=5000 \
        -e FLASK_ENV=production \
        -e LOG_LEVEL=$log_level \
        -v $(pwd)/logs:/app/logs \
        --restart unless-stopped \
        python-server-error
    
    print_status "Container started successfully with LOG_LEVEL=$log_level!"
    print_status "Server is running at http://localhost:5000"
    print_status "Logs are available in ./logs/ directory"
}

# Function to stop with docker-compose
stop_compose() {
    print_status "Stopping with docker-compose..."
    docker-compose down
    print_status "Services stopped successfully!"
}

# Function to show help
show_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build     Build the Docker image"
    echo "  run       Build and run the container"
    echo "  run-debug Run container with DEBUG logging"
    echo "  stop      Stop and remove the container"
    echo "  logs      Show container logs"
    echo "  status    Show container status"
    echo "  compose   Run with docker-compose"
    echo "  compose-stop Stop with docker-compose"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 run"
    echo "  $0 run-debug"
    echo "  $0 compose"
    echo "  $0 logs"
}

# Main script logic
case "${1:-help}" in
    build)
        check_docker
        build_image
        ;;
    run)
        check_docker
        stop_container
        build_image
        run_container
        ;;
    run-debug)
        check_docker
        stop_container
        build_image
        run_with_log_level DEBUG
        ;;
    stop)
        check_docker
        stop_container
        ;;
    logs)
        check_docker
        show_logs
        ;;
    status)
        check_docker
        show_status
        ;;
    compose)
        check_docker
        run_compose
        ;;
    compose-stop)
        check_docker
        stop_compose
        ;;
    help|*)
        show_help
        ;;
esac 