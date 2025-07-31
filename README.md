# python-server-error

A simple Flask-based Python server that can generate errors on demand for testing and debugging purposes.

## Features

- **Health Check Endpoint**: Monitor server status
- **Error Generation**: Enable/disable error generation on demand
- **Sample API**: Basic CRUD-like endpoints
- **CORS Support**: Cross-origin request support
- **Logging**: Comprehensive logging for debugging
- **Docker Support**: Containerized deployment

## Quick Start

### Option 1: Docker (Recommended)

#### Prerequisites
- Docker
- Docker Compose (optional)

#### Using Docker

1. **Build and run with Docker:**
```bash
# Build the image
docker build -t python-server-error .

# Run the container
docker run -d --name python-server-error -p 5000:5000 python-server-error
```

2. **Using the provided script:**
```bash
# Make script executable (if not already)
chmod +x docker-run.sh

# Build and run
./docker-run.sh run

# Stop the container
./docker-run.sh stop

# View logs
./docker-run.sh logs

# Check status
./docker-run.sh status
```

3. **Using Docker Compose:**
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

The server will be available at `http://localhost:5000`

### Option 2: Local Development

#### Prerequisites

- Python 3.7+
- pip

#### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd python-sample-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Basic Endpoints

- `GET /` - Home page with server information
- `GET /health` - Health check endpoint
- `GET /api/data` - Get all data items
- `GET /api/data/<id>` - Get specific data item by ID

### Error Management Endpoints

- `POST /error/enable` - Enable error generation
- `POST /error/disable` - Disable error generation  
- `GET /error/status` - Check error generation status
- `GET /trigger-error` - Trigger the intentional error (when enabled)

## Error Testing Workflow

### 1. Check Current Status
```bash
curl http://localhost:5000/error/status
```

### 2. Enable Error Generation
```bash
curl -X POST http://localhost:5000/error/enable
```

### 3. Trigger the Error
```bash
curl http://localhost:5000/trigger-error
```

This will return a 500 error with a `NameError` because `undefined_variable` is not defined.

### 4. Disable Error Generation
```bash
curl -X POST http://localhost:5000/error/disable
```

## The Intentional Error

The error is located in the `trigger_error()` function in `app.py`:

```python
@app.route('/trigger-error')
def trigger_error():
    """Endpoint that generates an error when enabled."""
    global error_enabled
    
    if error_enabled:
        # INTENTIONAL ERROR: This will cause a NameError because 'undefined_variable' is not defined
        # This is the error that can be fixed in a PR
        result = undefined_variable + "This should cause an error"
        return jsonify({'result': result})
    else:
        return jsonify({
            'message': 'Error generation is disabled. Enable it first with POST /error/enable',
            'status': 'disabled'
        })
```

## Fixing the Error

To fix this error, you would need to:

1. Define the `undefined_variable` or replace it with a valid variable
2. Create a pull request with the fix

Example fix:
```python
# Instead of:
result = undefined_variable + "This should cause an error"

# Use:
result = "Error triggered successfully" + " - This was the intentional error"
```

## Development

### Project Structure
```
python-sample-server/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── docker-run.sh      # Docker helper script
├── .dockerignore      # Docker ignore file
├── README.md          # This file
└── .gitignore         # Git ignore file
```

### Running in Development Mode

The server runs in debug mode by default, which provides:
- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

### Environment Variables

- `PORT` - Server port (default: 5000)

## Testing

You can test the endpoints using curl, Postman, or any HTTP client:

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test data endpoint
curl http://localhost:5000/api/data

# Test error workflow
curl -X POST http://localhost:5000/error/enable
curl http://localhost:5000/trigger-error
curl -X POST http://localhost:5000/error/disable
```

## Docker Management

### Building and Running

```bash
# Build the Docker image
docker build -t python-server-error .

# Run the container
docker run -d --name python-server-error -p 5000:5000 python-server-error

# Run in interactive mode (for debugging)
docker run -it --rm -p 5000:5000 python-server-error
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f python-server

# Stop all services
docker-compose down

# Rebuild and start
docker-compose up --build -d
```

### Using the Helper Script

The `docker-run.sh` script provides convenient commands:

```bash
# Show available commands
./docker-run.sh help

# Build and run
./docker-run.sh run

# Stop container
./docker-run.sh stop

# View logs
./docker-run.sh logs

# Check status
./docker-run.sh status

# Use docker-compose
./docker-run.sh compose
./docker-run.sh compose-stop
```

### Container Management

```bash
# List running containers
docker ps

# View container logs
docker logs python-server-error

# Execute commands in container
docker exec -it python-server-error /bin/bash

# Stop and remove container
docker stop python-server-error
docker rm python-server-error

# Remove image
docker rmi python-server-error
```

### Environment Variables

You can customize the container behavior with environment variables:

```bash
# Run with custom port
docker run -d --name python-server-error -p 8080:5000 -e PORT=5000 python-server-error

# Run with custom environment
docker run -d --name python-server-error -p 5000:5000 \
  -e FLASK_ENV=development \
  -e PORT=5000 \
  -e LOG_LEVEL=DEBUG \
  python-server-error

# Run with different log levels
docker run -d --name python-server-error -p 5000:5000 \
  -e LOG_LEVEL=DEBUG \
  -v $(pwd)/logs:/app/logs \
  python-server-error
```

### Docker Logging

The Docker container includes enhanced logging support:

```bash
# Run with DEBUG logging
./docker-run.sh run-debug

# Run with custom log level
docker run -d --name python-server-error -p 5000:5000 \
  -e LOG_LEVEL=WARNING \
  -v $(pwd)/logs:/app/logs \
  python-server-error

# View container logs
docker logs python-server-error

# View application logs (mounted volume)
ls -la logs/
cat logs/app.log
cat logs/error.log
```

### Health Checks

The container includes a health check that monitors the `/health` endpoint:

```bash
# Check container health
docker inspect python-server-error | grep Health -A 10
```

## Logging System

The application includes a comprehensive logging system with multiple log levels and file outputs.

### Log Files

- `logs/app.log` - All application logs
- `logs/error.log` - Error-level logs only
- `logs/debug.log` - Debug-level logs only

### Log Levels

- **DEBUG** - Detailed information for debugging
- **INFO** - General information about program execution
- **WARNING** - Warning messages for potentially problematic situations
- **ERROR** - Error messages for serious problems
- **CRITICAL** - Critical error messages for fatal problems

### Environment Variables

```bash
# Set log level
export LOG_LEVEL=DEBUG  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Run with specific log level
LOG_LEVEL=DEBUG python app.py
```

### Viewing Logs

#### Using the Log Management Script

```bash
# View all logs
./manage_logs.sh view app

# View error logs only
./manage_logs.sh errors

# View debug logs only
./manage_logs.sh debug

# Follow logs in real-time
./manage_logs.sh tail app

# Show log statistics
./manage_logs.sh stats

# Show log file sizes
./manage_logs.sh size

# Clear all logs
./manage_logs.sh clear all
```

#### Using the Log Viewer Script

```bash
# View all logs
python3 view_logs.py --file app

# View only ERROR level logs
python3 view_logs.py --file app --level ERROR

# View last 50 lines
python3 view_logs.py --file app --lines 50

# Filter by message pattern
python3 view_logs.py --file app --message "error"

# Filter by time range
python3 view_logs.py --file app --since "2024-01-01 10:00:00" --until "2024-01-01 11:00:00"

# Follow logs (like tail -f)
python3 view_logs.py --file app --follow

# Show statistics
python3 view_logs.py --file app --stats
```

#### Manual Log Viewing

```bash
# View all logs
cat logs/app.log

# View error logs
cat logs/error.log

# View debug logs
cat logs/debug.log

# Follow logs
tail -f logs/app.log

# View last 100 lines
tail -n 100 logs/app.log

# Search for specific patterns
grep "ERROR" logs/app.log
grep "trigger-error" logs/app.log
```

### Log Format

Log entries follow this format:
```
2024-01-01 12:00:00 - module_name - LEVEL - message
```

Example:
```
2024-01-01 12:00:00 - app - INFO - Home endpoint accessed - IP: 127.0.0.1
2024-01-01 12:00:01 - app - WARNING - Error generation enabled by IP: 127.0.0.1
2024-01-01 12:00:02 - app - ERROR - Intentional error triggered by IP: 127.0.0.1
```

### Docker Logging

When running in Docker, logs are also available through Docker commands:

```bash
# View container logs
docker logs python-server-error

# Follow container logs
docker logs -f python-server-error

# View last 100 lines
docker logs --tail 100 python-server-error
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test your changes
5. Submit a pull request

## License

This project is open source and available under the MIT License. 
