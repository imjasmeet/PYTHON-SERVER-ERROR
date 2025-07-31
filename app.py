from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import logging
import sys
from datetime import datetime

# Enhanced logging configuration
def setup_logging():
    """Setup logging with different levels and formatting."""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            # Console handler with INFO level
            logging.StreamHandler(sys.stdout),
            # File handler for all logs
            logging.FileHandler('logs/app.log'),
            # File handler for errors only
            logging.FileHandler('logs/error.log'),
            # File handler for debug logs
            logging.FileHandler('logs/debug.log')
        ]
    )
    
    # Set specific levels for handlers
    root_logger = logging.getLogger()
    
    # Set error handler level
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler) and 'error.log' in handler.baseFilename:
            handler.setLevel(logging.ERROR)
        elif isinstance(handler, logging.FileHandler) and 'debug.log' in handler.baseFilename:
            handler.setLevel(logging.DEBUG)
    
    # Set Flask logger level
    logging.getLogger('werkzeug').setLevel(logging.INFO)
    
    return logging.getLogger(__name__)

# Setup logging
logger = setup_logging()

app = Flask(__name__)
CORS(app)

# Global variable to track error state
error_enabled = False

@app.route('/')
def home():
    """Home endpoint that returns basic server information."""
    logger.info(f"Home endpoint accessed - IP: {request.remote_addr}")
    return jsonify({
        'message': 'Python Sample Server is running!',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    """Health check endpoint."""
    logger.debug(f"Health check requested - IP: {request.remote_addr}")
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/error/enable', methods=['POST'])
def enable_error():
    """Enable error generation on demand."""
    global error_enabled
    error_enabled = True
    logger.warning(f"Scenario generation enabled by IP: {request.remote_addr}")
    return jsonify({
        'message': 'Error generation enabled',
        'status': 'enabled'
    })

@app.route('/error/disable', methods=['POST'])
def disable_error():
    """Disable error generation."""
    global error_enabled
    error_enabled = False
    logger.info(f"Error generation disabled by IP: {request.remote_addr}")
    return jsonify({
        'message': 'Error generation disabled',
        'status': 'disabled'
    })

@app.route('/error/status')
def error_status():
    """Check current error generation status."""
    logger.debug(f"Error status checked - IP: {request.remote_addr}, Status: {error_enabled}")
    return jsonify({
        'error_enabled': error_enabled,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/trigger-error')
def trigger_error():
    """Endpoint that generates an error when enabled."""
    global error_enabled
    
    logger.info(f"Trigger error endpoint accessed - IP: {request.remote_addr}, Error enabled: {error_enabled}")
    
    if error_enabled:
        # INTENTIONAL ERROR: This will cause a NameError because 'undefined_variable' is not defined
        # This is the error that can be fixed in a PR
        logger.debug(f"Intentional error triggered by IP: {request.remote_addr}")
        try:
            result = undefined_variable + "This should cause an error"
            return jsonify({'result': result})
        except NameError as e:
            import traceback
            error_traceback = traceback.format_exc().replace('\n', ' ')
            logger.debug(f"NameError occurred: {str(e)}")
            logger.error(f"Full traceback: {error_traceback}")
            raise  # Re-raise the exception for Flask to handle
    else:
        logger.debug(f"Error trigger attempted but disabled - IP: {request.remote_addr}")
        return jsonify({
            'message': 'Error generation is disabled. Enable it first with POST /error/enable',
            'status': 'disabled'
        })

@app.route('/api/data', methods=['GET'])
def get_data():
    """Sample API endpoint that returns some data."""
    logger.info(f"API data endpoint accessed - IP: {request.remote_addr}")
    return jsonify({
        'data': [
            {'id': 1, 'name': 'Item 1', 'value': 100},
            {'id': 2, 'name': 'Item 2', 'value': 200},
            {'id': 3, 'name': 'Item 3', 'value': 300}
        ],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/data/<int:item_id>', methods=['GET'])
def get_data_item(item_id):
    """Get a specific data item by ID."""
    logger.info(f"API data item requested - IP: {request.remote_addr}, Item ID: {item_id}")
    
    data = [
        {'id': 1, 'name': 'Item 1', 'value': 100},
        {'id': 2, 'name': 'Item 2', 'value': 200},
        {'id': 3, 'name': 'Item 3', 'value': 300}
    ]
    
    item = next((item for item in data if item['id'] == item_id), None)
    
    if item:
        logger.debug(f"Item found - ID: {item_id}")
        return jsonify(item)
    else:
        logger.warning(f"Item not found - IP: {request.remote_addr}, Item ID: {item_id}")
        return jsonify({'error': 'Item not found'}), 404

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.warning(f"404 error - IP: {request.remote_addr}, Path: {request.path}")
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    import traceback
    error_traceback = traceback.format_exc().replace('\n', ' ')
    logger.error(f"500 error - IP: {request.remote_addr}, Path: {request.path}, Error: {str(error)}")
    logger.error(f"Full traceback: {error_traceback}")
    return jsonify({'error': 'Internal server error'}), 500

@app.before_request
def log_request():
    """Log all incoming requests."""
    logger.debug(f"Request: {request.method} {request.path} - IP: {request.remote_addr}")

@app.after_request
def log_response(response):
    """Log all outgoing responses."""
    logger.debug(f"Response: {response.status_code} for {request.method} {request.path}")
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True) 