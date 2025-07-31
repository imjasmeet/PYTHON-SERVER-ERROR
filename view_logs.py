#!/usr/bin/env python3
"""
Log viewer script for the Flask application.
This script provides various ways to view and filter logs.
"""

import os
import sys
import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path

# Log file paths
LOG_FILES = {
    'app': 'logs/app.log',
    'error': 'logs/error.log',
    'debug': 'logs/debug.log'
}

# Log level colors for terminal output
LOG_COLORS = {
    'DEBUG': '\033[36m',    # Cyan
    'INFO': '\033[32m',     # Green
    'WARNING': '\033[33m',  # Yellow
    'ERROR': '\033[31m',    # Red
    'CRITICAL': '\033[35m', # Magenta
    'RESET': '\033[0m'      # Reset
}

def colorize_log_level(level):
    """Add color to log level."""
    color = LOG_COLORS.get(level, LOG_COLORS['RESET'])
    return f"{color}{level}{LOG_COLORS['RESET']}"

def parse_log_line(line):
    """Parse a log line and return structured data."""
    # Expected format: 2024-01-01 12:00:00 - module_name - LEVEL - message
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - ([^-]+) - (\w+) - (.+)'
    match = re.match(pattern, line.strip())
    
    if match:
        timestamp, module, level, message = match.groups()
        return {
            'timestamp': timestamp,
            'module': module,
            'level': level,
            'message': message,
            'raw': line.strip()
        }
    return None

def filter_logs(logs, level=None, module=None, message_pattern=None, time_range=None):
    """Filter logs based on various criteria."""
    filtered_logs = []
    
    for log in logs:
        if log is None:
            continue
            
        # Filter by level
        if level and log['level'] != level.upper():
            continue
            
        # Filter by module
        if module and module.lower() not in log['module'].lower():
            continue
            
        # Filter by message pattern
        if message_pattern and not re.search(message_pattern, log['message'], re.IGNORECASE):
            continue
            
        # Filter by time range
        if time_range:
            try:
                log_time = datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S')
                if log_time < time_range[0] or log_time > time_range[1]:
                    continue
            except ValueError:
                continue
                
        filtered_logs.append(log)
    
    return filtered_logs

def read_log_file(file_path, lines=None):
    """Read log file and return parsed logs."""
    if not os.path.exists(file_path):
        print(f"Log file not found: {file_path}")
        return []
    
    with open(file_path, 'r') as f:
        if lines:
            # Read last N lines
            all_lines = f.readlines()
            file_lines = all_lines[-lines:]
        else:
            file_lines = f.readlines()
    
    logs = []
    for line in file_lines:
        parsed = parse_log_line(line)
        if parsed:
            logs.append(parsed)
    
    return logs

def display_logs(logs, show_timestamp=True, show_module=True, colorize=True):
    """Display logs in a formatted way."""
    for log in logs:
        output_parts = []
        
        if show_timestamp:
            output_parts.append(log['timestamp'])
        
        if show_module:
            output_parts.append(f"[{log['module']}]")
        
        level = log['level']
        if colorize:
            level = colorize_log_level(level)
        output_parts.append(f"[{level}]")
        
        output_parts.append(log['message'])
        
        print(' '.join(output_parts))

def get_log_statistics(logs):
    """Get statistics about the logs."""
    stats = {
        'total': len(logs),
        'by_level': {},
        'by_module': {},
        'time_range': None
    }
    
    if not logs:
        return stats
    
    # Count by level and module
    for log in logs:
        level = log['level']
        module = log['module']
        
        stats['by_level'][level] = stats['by_level'].get(level, 0) + 1
        stats['by_module'][module] = stats['by_module'].get(module, 0) + 1
    
    # Get time range
    timestamps = [log['timestamp'] for log in logs if log['timestamp']]
    if timestamps:
        try:
            times = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in timestamps]
            stats['time_range'] = (min(times), max(times))
        except ValueError:
            pass
    
    return stats

def print_statistics(stats):
    """Print log statistics."""
    print(f"\n=== Log Statistics ===")
    print(f"Total log entries: {stats['total']}")
    
    if stats['time_range']:
        start, end = stats['time_range']
        print(f"Time range: {start} to {end}")
    
    print(f"\nBy Level:")
    for level, count in sorted(stats['by_level'].items()):
        print(f"  {level}: {count}")
    
    print(f"\nBy Module:")
    for module, count in sorted(stats['by_module'].items()):
        print(f"  {module}: {count}")

def main():
    parser = argparse.ArgumentParser(description='View Flask application logs')
    parser.add_argument('--file', choices=['app', 'error', 'debug'], default='app',
                       help='Log file to view (default: app)')
    parser.add_argument('--level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                       help='Filter by log level')
    parser.add_argument('--module', help='Filter by module name')
    parser.add_argument('--message', help='Filter by message pattern (regex)')
    parser.add_argument('--lines', type=int, help='Show last N lines')
    parser.add_argument('--since', help='Show logs since time (YYYY-MM-DD HH:MM:SS)')
    parser.add_argument('--until', help='Show logs until time (YYYY-MM-DD HH:MM:SS)')
    parser.add_argument('--no-color', action='store_true', help='Disable color output')
    parser.add_argument('--no-timestamp', action='store_true', help='Hide timestamps')
    parser.add_argument('--no-module', action='store_true', help='Hide module names')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--follow', action='store_true', help='Follow log file (like tail -f)')
    
    args = parser.parse_args()
    
    # Determine time range
    time_range = None
    if args.since or args.until:
        start_time = None
        end_time = None
        
        if args.since:
            try:
                start_time = datetime.strptime(args.since, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                print("Invalid since time format. Use YYYY-MM-DD HH:MM:SS")
                sys.exit(1)
        
        if args.until:
            try:
                end_time = datetime.strptime(args.until, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                print("Invalid until time format. Use YYYY-MM-DD HH:MM:SS")
                sys.exit(1)
        
        time_range = (start_time, end_time)
    
    # Read logs
    log_file = LOG_FILES[args.file]
    logs = read_log_file(log_file, args.lines)
    
    # Filter logs
    filtered_logs = filter_logs(
        logs,
        level=args.level,
        module=args.module,
        message_pattern=args.message,
        time_range=time_range
    )
    
    # Display logs
    if not args.follow:
        display_logs(
            filtered_logs,
            show_timestamp=not args.no_timestamp,
            show_module=not args.no_module,
            colorize=not args.no_color
        )
        
        if args.stats:
            stats = get_log_statistics(filtered_logs)
            print_statistics(stats)
    else:
        # Follow mode
        print(f"Following {log_file}... (Press Ctrl+C to stop)")
        try:
            with open(log_file, 'r') as f:
                # Go to end of file
                f.seek(0, 2)
                
                while True:
                    line = f.readline()
                    if line:
                        parsed = parse_log_line(line)
                        if parsed:
                            filtered = filter_logs([parsed], args.level, args.module, args.message, time_range)
                            if filtered:
                                display_logs(
                                    filtered,
                                    show_timestamp=not args.no_timestamp,
                                    show_module=not args.no_module,
                                    colorize=not args.no_color
                                )
                    else:
                        import time
                        time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nStopped following logs.")

if __name__ == '__main__':
    main() 