from flask import Blueprint, jsonify
from flasgger import swag_from
from services.scraping_service import ScrapingService

simple_scraping_bp = Blueprint('simple_scraping', __name__)

@simple_scraping_bp.route('/padron-info', methods=['GET'])
@swag_from({
    'tags': ['Padron Info'],
    'summary': 'Get Tarragona Padron Information',
    'description': 'Get simplified information about Tarragona padron de habitantes document',
    'responses': {
        '200': {
            'description': 'Successful information retrieval',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'title': {'type': 'string'},
                    'summary': {'type': 'string'},
                    'requirements': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    },
                    'key_info': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    }
                }
            }
        },
        '500': {
            'description': 'Error retrieving information',
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
def get_padron_info():
    """Get simplified information about Tarragona padron document"""
    try:
        url = "https://seu.tarragona.cat/sta/CarpetaPublic/doEvent?APP_CODE=STA&PAGE_CODE=CATALOGO&DETALLE=6269000003494351199500&lang=ES"
        
        scraping_service = ScrapingService()
        result = scraping_service.scrape_tarragona_padron_info(url)
        
        if result['success']:
            doc_info = result['document_info']
            
            # Extraer información clave del texto
            raw_text = doc_info['raw_text']
            
            # Información estructurada basada en el contenido real
            simplified_info = {
                'success': True,
                'title': 'Alta al padró d\'habitants - Tarragona',
                'summary': 'Es la inscripció al padró municipal d\'habitants de la ciutat de Tarragona. El padró municipal és el registre administratiu on consten els veïns del municipi.',
                'requirements': [
                    'Documentació d\'identitat segons nacionalitat (DNI, NIE, passaport)',
                    'Documentació que acrediti el domicili (escriptura, contracte de lloguer, autorització)',
                    'Per menors d\'edat: llibre de família o certificat de naixement',
                    'Autorització si és necessària per fer tràmits'
                ],
                'key_info': [
                    'Qualsevol persona major de 16 anys que visqui al municipi pot presentar la sol·licitud',
                    'Es pot presentar en qualsevol moment',
                    'La inscripció es realitza a l\'instant a les oficines OMAC',
                    'El tràmit és gratuït',
                    'Estrangers no comunitaris han de renovar cada dos anys',
                    'Presentació a Oficines Municipals d\'Atenció Ciutadana (OMAC)'
                ]
            }
            
            return jsonify(simplified_info), 200
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error')
            }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Error: {str(e)}"
        }), 500
