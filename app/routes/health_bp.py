from flask import Blueprint, jsonify
from services.health_service import HealthService
from flasgger import swag_from

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
@swag_from({
    'tags': ['Health'],
    'summary': 'Health Check Endpoint',
    'description': 'Check if the API service is running and healthy',
    'responses': {
        '200': {
            'description': 'Successful health check',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'message': {'type': 'string'},
                    'timestamp': {'type': 'string'},
                    'version': {'type': 'string'}
                }
            }
        }
    }
})
def health_check():
    """Health check endpoint"""
    service_response = HealthService.health_check()
    return jsonify(service_response), 200

@health_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Health'],
    'summary': 'Root Endpoint',
    'description': 'Basic API status endpoint',
    'responses': {
        '200': {
            'description': 'API Status',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'message': {'type': 'string'},
                    'version': {'type': 'string'}
                }
            }
        }
    }
})
def root():
    """Root endpoint"""
    return jsonify({
        'status': 'Working',
        'message': 'Flask API is running!',
        'version': '1.0.0'
    }), 200