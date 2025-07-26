from flask import Blueprint, jsonify, request
from flasgger import swag_from

from models.user_model import UserModel
from services.auth_service import AuthService
from config.db_settings import DbSettings

db_settings = DbSettings()

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'summary': 'User Login',
    'description': 'Authenticate user with username and password',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['username', 'password'],
                'properties': {
                    'username': {
                        'type': 'string',
                        'description': 'Username'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Password'
                    }
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Successful authentication',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'message': {'type': 'string'},
                    'token': {'type': 'string'}
                }
            }
        },
        '401': {
            'description': 'Unauthorized',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'message': {'type': 'string'}
                }
            }
        },
        '400': {
            'description': 'Bad request',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def login():
    """Login endpoint"""
    try:
        # Validate request data
        if not request.json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        username = request.json.get('username')
        password = request.json.get('password')
        
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        _user = UserModel(username=username, password=password)

        auth_service = AuthService(db_settings=db_settings)

        is_authenticated = auth_service.authenticate_user(_user)

        if is_authenticated:
            encoded_token = auth_service.encode_auth_token(_user)
            return jsonify({
                'status': 'success',
                'message': 'User authenticated successfully',
                'token': encoded_token
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized'
            }), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 400
