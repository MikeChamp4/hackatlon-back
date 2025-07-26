from flask import Blueprint, jsonify, request
from flasgger import swag_from
from services.scraping_service import ScrapingService

scraping_bp = Blueprint('scraping', __name__)

@scraping_bp.route('/scrape/tarragona-padron', methods=['POST'])
@swag_from({
    'tags': ['Web Scraping'],
    'summary': 'Scrape Tarragona Padron Information',
    'description': 'Extract document information from Tarragona padron de habitantes webpage',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['url'],
                'properties': {
                    'url': {
                        'type': 'string',
                        'description': 'URL of the Tarragona padron webpage to scrape',
                        'example': 'https://seu.tarragona.cat/sta/CarpetaPublic/doEvent?APP_CODE=STA&PAGE_CODE=CATALOGO&DETALLE=6269000003494351199500&lang=ES'
                    }
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Successful scraping',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'url': {'type': 'string'},
                    'document_info': {
                        'type': 'object',
                        'properties': {
                            'title': {'type': 'string'},
                            'description': {'type': 'string'},
                            'requirements': {
                                'type': 'array',
                                'items': {'type': 'string'}
                            },
                            'procedures': {
                                'type': 'array',
                                'items': {'type': 'string'}
                            },
                            'additional_info': {
                                'type': 'array',
                                'items': {'type': 'string'}
                            },
                            'raw_text': {'type': 'string'}
                        }
                    },
                    'status_code': {'type': 'integer'}
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
        },
        '500': {
            'description': 'Scraping failed',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'error': {'type': 'string'},
                    'url': {'type': 'string'}
                }
            }
        }
    }
})
def scrape_tarragona_padron():
    """Scrape Tarragona padron webpage for document information"""
    try:
        # Validate request data
        if not request.json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        url = request.json.get('url')
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        # Validate that it's a Tarragona URL for security
        if 'tarragona.cat' not in url:
            return jsonify({"error": "Only Tarragona official URLs are allowed"}), 400
        
        # Perform scraping
        scraping_service = ScrapingService()
        result = scraping_service.scrape_tarragona_padron_info(url)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }), 500


@scraping_bp.route('/scrape/tarragona-padron/quick', methods=['GET'])
@swag_from({
    'tags': ['Web Scraping'],
    'summary': 'Quick Scrape Default Tarragona Padron Page',
    'description': 'Extract document information from the default Tarragona padron de habitantes webpage',
    'responses': {
        '200': {
            'description': 'Successful scraping',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'url': {'type': 'string'},
                    'document_info': {
                        'type': 'object',
                        'properties': {
                            'title': {'type': 'string'},
                            'description': {'type': 'string'},
                            'requirements': {
                                'type': 'array',
                                'items': {'type': 'string'}
                            },
                            'procedures': {
                                'type': 'array',
                                'items': {'type': 'string'}
                            },
                            'additional_info': {
                                'type': 'array',
                                'items': {'type': 'string'}
                            },
                            'raw_text': {'type': 'string'}
                        }
                    },
                    'status_code': {'type': 'integer'}
                }
            }
        },
        '500': {
            'description': 'Scraping failed',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'error': {'type': 'string'},
                    'url': {'type': 'string'}
                }
            }
        }
    }
})
def scrape_tarragona_padron_quick():
    """Quick scrape of the default Tarragona padron webpage"""
    try:
        # URL por defecto que proporcionaste
        default_url = "https://seu.tarragona.cat/sta/CarpetaPublic/doEvent?APP_CODE=STA&PAGE_CODE=CATALOGO&DETALLE=6269000003494351199500&lang=ES"
        
        # Perform scraping
        scraping_service = ScrapingService()
        result = scraping_service.scrape_tarragona_padron_info(default_url)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }), 500
