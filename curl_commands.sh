#!/bin/bash

# Curl commands for python-server-error Flask application
# Base URL - change this if your server is running on a different host/port
BASE_URL="http://localhost:5000"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Python Server Error - Curl Commands ===${NC}"
echo "Base URL: $BASE_URL"
echo ""

# Function to print section headers
print_section() {
    echo -e "${GREEN}=== $1 ===${NC}"
    echo ""
}

# Function to print command with description
print_command() {
    echo -e "${YELLOW}$1${NC}"
    echo "$2"
    echo ""
}

# Basic Endpoints
print_section "Basic Endpoints"

print_command "GET / - Home endpoint" "curl $BASE_URL/"
print_command "GET /health - Health check" "curl $BASE_URL/health"

# Error Management Endpoints
print_section "Error Management Endpoints"

print_command "GET /error/status - Check error status" "curl $BASE_URL/error/status"
print_command "POST /error/enable - Enable error generation" "curl -X POST $BASE_URL/error/enable"
print_command "POST /error/disable - Disable error generation" "curl -X POST $BASE_URL/error/disable"
print_command "GET /trigger-error - Trigger intentional error" "curl $BASE_URL/trigger-error"

# API Data Endpoints
print_section "API Data Endpoints"

print_command "GET /api/data - Get all data items" "curl $BASE_URL/api/data"
print_command "GET /api/data/1 - Get specific item (ID 1)" "curl $BASE_URL/api/data/1"
print_command "GET /api/data/2 - Get specific item (ID 2)" "curl $BASE_URL/api/data/2"
print_command "GET /api/data/3 - Get specific item (ID 3)" "curl $BASE_URL/api/data/3"
print_command "GET /api/data/999 - Get non-existent item (404)" "curl $BASE_URL/api/data/999"

# Error Testing Workflow
print_section "Error Testing Workflow"

echo -e "${YELLOW}Complete error testing workflow:${NC}"
echo "1. Check current error status:"
echo "   curl $BASE_URL/error/status"
echo ""
echo "2. Enable error generation:"
echo "   curl -X POST $BASE_URL/error/enable"
echo ""
echo "3. Trigger the error (will return 500):"
echo "   curl $BASE_URL/trigger-error"
echo ""
echo "4. Disable error generation:"
echo "   curl -X POST $BASE_URL/error/disable"
echo ""

# Pretty-printed versions
print_section "Pretty-Printed Commands (with jq)"

print_command "GET / - Home endpoint (pretty)" "curl -s $BASE_URL/ | jq '.'"
print_command "GET /health - Health check (pretty)" "curl -s $BASE_URL/health | jq '.'"
print_command "GET /api/data - Get all data (pretty)" "curl -s $BASE_URL/api/data | jq '.'"
print_command "GET /error/status - Error status (pretty)" "curl -s $BASE_URL/error/status | jq '.'"

# Verbose versions for debugging
print_section "Verbose Commands (with headers)"

print_command "GET / - Home endpoint (verbose)" "curl -v $BASE_URL/"
print_command "POST /error/enable - Enable error (verbose)" "curl -v -X POST $BASE_URL/error/enable"
print_command "GET /trigger-error - Trigger error (verbose)" "curl -v $BASE_URL/trigger-error"

# Testing with different content types
print_section "Testing with Headers"

print_command "GET /api/data with Accept header" "curl -H 'Accept: application/json' $BASE_URL/api/data"
print_command "POST /error/enable with Content-Type" "curl -H 'Content-Type: application/json' -X POST $BASE_URL/error/enable"

# Error scenarios
print_section "Error Scenarios"

print_command "GET non-existent endpoint (404)" "curl $BASE_URL/non-existent"
print_command "POST to GET-only endpoint (405)" "curl -X POST $BASE_URL/health"

# Performance testing
print_section "Performance Testing"

print_command "Health check (timing)" "curl -w '@-' -o /dev/null -s $BASE_URL/health <<< 'time_namelookup:  %{time_namelookup}\ntime_connect:      %{time_connect}\ntime_appconnect:   %{time_appconnect}\ntime_pretransfer:  %{time_pretransfer}\ntime_redirect:     %{time_redirect}\ntime_starttransfer: %{time_starttransfer}\n----------\ntime_total:        %{time_total}\n'"

# Batch testing script
print_section "Batch Testing"

echo -e "${YELLOW}Create a batch test script:${NC}"
echo "#!/bin/bash"
echo "echo 'Testing all endpoints...'"
echo "curl -s $BASE_URL/health | jq -r '.status'"
echo "curl -s $BASE_URL/error/status | jq -r '.error_enabled'"
echo "curl -s -X POST $BASE_URL/error/enable | jq -r '.status'"
echo "curl -s $BASE_URL/trigger-error | jq -r '.error // .message'"
echo "curl -s -X POST $BASE_URL/error/disable | jq -r '.status'"
echo ""

# Docker-specific commands
print_section "Docker-Specific Commands"

echo -e "${YELLOW}If running in Docker container:${NC}"
echo "curl http://localhost:5000/health"
echo "curl http://localhost:5000/"
echo ""

# Environment-specific URLs
print_section "Environment-Specific URLs"

echo -e "${YELLOW}For different environments:${NC}"
echo "Local:     curl http://localhost:5000/health"
echo "Docker:    curl http://localhost:5000/health"
echo "Remote:    curl http://your-server-ip:5000/health"
echo ""

echo -e "${BLUE}=== End of Curl Commands ===${NC}"
echo "Note: Make sure your Flask server is running before executing these commands."
echo "You can start it with: python app.py or ./docker-run.sh run" 