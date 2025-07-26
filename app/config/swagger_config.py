import json
import os

def load_swagger_template():
    """Load Swagger template from JSON file"""
    config_dir = os.path.dirname(__file__)
    json_path = os.path.join(config_dir, 'swagger_spec.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Swagger spec file not found at {json_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing Swagger JSON: {e}")
        return {}

# Load template from JSON file
template = load_swagger_template()

# Swagger UI configuration
swagger_config = {
    "headers": [],
    "specs": [{
        "endpoint": 'apispec',
        "route": '/apispec.json',
        "rule_filter": lambda rule: True,
        "model_filter": lambda tag: True,
    }],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs",
    "swagger_ui_config": {
        "displayRequestDuration": True,
        "docExpansion": "none",
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "defaultModelsExpandDepth": 2,
        "defaultModelExpandDepth": 2
    }
}
