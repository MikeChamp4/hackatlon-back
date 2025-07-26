from flask import Flask
from flasgger import Swagger
from config.db_settings import DbSettings
from routes.health_bp import health_bp
from routes.auth_bp import auth_bp
from routes.scraping_bp import scraping_bp
from routes.simple_scraping_bp import simple_scraping_bp
from config.swagger_config import swagger_config, template
from dotenv import load_dotenv
import os

# Load environment variables with explicit path
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)

db_settings = DbSettings()

app = Flask(__name__)

# Initialize Swagger
swagger = Swagger(
    app,
    template=template,
    config=swagger_config
)

# Register blueprints
app.register_blueprint(health_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(scraping_bp)
app.register_blueprint(simple_scraping_bp)

if __name__ == '__main__':
    print("🚀 Starting Flask app with Swagger UI...")
    print("📖 Swagger UI available at: http://localhost:8000/docs")
    print("🏥 Health check at: http://localhost:8000/health")
    print("🔐 Login endpoint at: http://localhost:8000/login")
    print("🌐 Web scraping endpoint at: http://localhost:8000/scrape/tarragona-padron/quick")
    print("📄 Padron info endpoint at: http://localhost:8000/padron-info")
    app.run(debug=True, host='0.0.0.0', port=8000)
