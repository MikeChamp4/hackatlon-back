from flask_cors import CORS

def configure_cors(app):
    """
    Configurar CORS para la aplicación Flask
    """
    # Configuración de CORS
    cors_config = {
        # Orígenes permitidos (usa "*" para permitir todos)
        "origins": ["*"],
        
        # Métodos HTTP permitidos
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        
        # Headers permitidos
        "allow_headers": [
            "Content-Type", 
            "Authorization", 
            "X-Requested-With",
            "Accept",
            "Origin",
            "Access-Control-Request-Method",
            "Access-Control-Request-Headers"
        ],
        
        # Permitir envío de credenciales (cookies, headers de autorización)
        "supports_credentials": True,
        
        # Headers expuestos al cliente
        "expose_headers": ["Content-Range", "X-Content-Range"],
        
        # Tiempo de cache para preflight requests (en segundos)
        "max_age": 3600
    }
    
    # Aplicar configuración CORS
    CORS(app, **cors_config)
    
    return app

def configure_cors_strict(app):
    """
    Configuración CORS más restrictiva para producción
    """
    cors_config = {
        # Solo orígenes específicos en producción
        "origins": [
            "http://localhost:3000",      # React dev server
            "http://localhost:5173",      # Vite dev server  
            "http://localhost:8080",      # Vue dev server
            "https://tu-dominio.com",     # Dominio de producción
        ],
        
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "max_age": 86400  # 24 horas
    }
    
    CORS(app, **cors_config)
    return app
