#!/bin/bash

# Log management script for python-server-error Flask application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Function to show help
show_help() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  view [file]     View logs (app, error, debug)"
    echo "  tail [file]     Follow logs in real-time"
    echo "  errors          View only error logs"
    echo "  debug           View debug logs"
    echo "  stats           Show log statistics"
    echo "  clear [file]    Clear log files"
    echo "  size            Show log file sizes"
    echo "  help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 view app"
    echo "  $0 tail error"
    echo "  $0 errors"
    echo "  $0 clear all"
    echo "  $0 stats"
}

# Function to check if logs directory exists
check_logs_dir() {
    if [ ! -d "logs" ]; then
        print_error "Logs directory not found. Run the application first to generate logs."
        exit 1
    fi
}

# Function to view logs
view_logs() {
    local file=${1:-app}
    check_logs_dir
    
    case $file in
        app|error|debug)
            print_status "Viewing $file logs..."
            python3 view_logs.py --file $file
            ;;
        *)
            print_error "Invalid log file: $file. Use app, error, or debug."
            exit 1
            ;;
    esac
}

# Function to follow logs
tail_logs() {
    local file=${1:-app}
    check_logs_dir
    
    case $file in
        app|error|debug)
            print_status "Following $file logs..."
            python3 view_logs.py --file $file --follow
            ;;
        *)
            print_error "Invalid log file: $file. Use app, error, or debug."
            exit 1
            ;;
    esac
}

# Function to view error logs
view_errors() {
    check_logs_dir
    print_status "Viewing error logs..."
    python3 view_logs.py --file error --level ERROR
}

# Function to view debug logs
view_debug() {
    check_logs_dir
    print_status "Viewing debug logs..."
    python3 view_logs.py --file debug --level DEBUG
}

# Function to show log statistics
show_stats() {
    check_logs_dir
    print_status "Showing log statistics..."
    python3 view_logs.py --file app --stats
}

# Function to clear logs
clear_logs() {
    local file=${1:-all}
    check_logs_dir
    
    case $file in
        all)
            print_warning "Clearing all log files..."
            rm -f logs/*.log
            print_status "All log files cleared."
            ;;
        app)
            print_warning "Clearing app.log..."
            rm -f logs/app.log
            print_status "app.log cleared."
            ;;
        error)
            print_warning "Clearing error.log..."
            rm -f logs/error.log
            print_status "error.log cleared."
            ;;
        debug)
            print_warning "Clearing debug.log..."
            rm -f logs/debug.log
            print_status "debug.log cleared."
            ;;
        *)
            print_error "Invalid log file: $file. Use all, app, error, or debug."
            exit 1
            ;;
    esac
}

# Function to show log file sizes
show_sizes() {
    check_logs_dir
    
    print_header "Log File Sizes"
    echo ""
    
    if [ -f "logs/app.log" ]; then
        size=$(du -h logs/app.log | cut -f1)
        echo "app.log: $size"
    else
        echo "app.log: Not found"
    fi
    
    if [ -f "logs/error.log" ]; then
        size=$(du -h logs/error.log | cut -f1)
        echo "error.log: $size"
    else
        echo "error.log: Not found"
    fi
    
    if [ -f "logs/debug.log" ]; then
        size=$(du -h logs/debug.log | cut -f1)
        echo "debug.log: $size"
    else
        echo "debug.log: Not found"
    fi
    
    echo ""
    print_status "Total logs directory size:"
    du -sh logs/
}

# Function to show log levels
show_levels() {
    print_header "Available Log Levels"
    echo ""
    python3 logging_config.py
}

# Main script logic
case "${1:-help}" in
    view)
        view_logs $2
        ;;
    tail)
        tail_logs $2
        ;;
    errors)
        view_errors
        ;;
    debug)
        view_debug
        ;;
    stats)
        show_stats
        ;;
    clear)
        clear_logs $2
        ;;
    size)
        show_sizes
        ;;
    levels)
        show_levels
        ;;
    help|*)
        show_help
        ;;
esac 