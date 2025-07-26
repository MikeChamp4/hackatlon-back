from flask import Blueprint, request, jsonify
from config.ollama_settings import OllamaSettings 
from services.chat_service import ChatService
from flasgger import swag_from

chat_bp = Blueprint('chat', __name__)

ollama_settings = OllamaSettings()

@chat_bp.route('/chat', methods=['POST'])
@swag_from({
    'tags': ['Chat'],
    'summary': 'Chat with Gemma:7B Model',
    'description': 'Send a query to the local Gemma:7B model and get a response',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'query': {
                        'type': 'string',
                        'description': 'The user query to send to the model',
                        'example': 'Explícame qué es la inteligencia artificial'
                    }
                },
                'required': ['query']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Successful response from the model',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'response': {'type': 'string'},
                    'model': {'type': 'string'},
                    'query': {'type': 'string'}
                }
            }
        },
        '400': {
            'description': 'Bad request - missing or invalid query',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        '500': {
            'description': 'Internal server error',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def chat():
    """
    Endpoint para chatear con el modelo Gemma:7B
    Recibe una query del usuario y retorna la respuesta del modelo
    """
    
    try:
        # Obtener los datos del request
        data = request.get_json()
        
        # Validar que se haya enviado la query
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Se requiere el campo "query" en el body del request'
            }), 400
        
        query: str = data['query'].strip()
        
        # Validar que la query no esté vacía
        if not query:
            return jsonify({
                'error': 'La query no puede estar vacía'
            }), 400

        chat_service = ChatService(ollama_settings=ollama_settings)

        # Llamar al servicio de chat
        response = chat_service.send_message(query=query)

        
        # Si hubo un error en el servicio, retornar error 500
        if not response.get('success', False):
            return jsonify({
                'success': False,
                'error': response.get('error', 'Error desconocido')
            }), 500
        
        # Retornar la respuesta exitosa
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

@chat_bp.route('/chat/model-info', methods=['GET'])
@swag_from({
    'tags': ['Chat'],
    'summary': 'Get Model Information',
    'description': 'Get information about the current Gemma:7B model',
    'responses': {
        '200': {
            'description': 'Model information retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'model_info': {
                        'type': 'object',
                        'properties': {
                            'name': {'type': 'string'},
                            'size': {'type': 'string'},
                            'modified_at': {'type': 'string'}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Error retrieving model information',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def get_model_info():
    """
    Endpoint para obtener información sobre el modelo Gemma:7B
    """
    try:
        response = ChatService.get_model_info()
        
        if not response.get('success', False):
            return jsonify(response), 500
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }), 500
