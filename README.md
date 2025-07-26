# Hackatlon Backend - Flask API

A robust Flask-based REST API with MySQL database integration and AI chat capabilities, designed for hackathon projects.

## 🚀 Features

- **Flask Framework**: Modern Python web framework
- **MySQL Database**: With SQLAlchemy ORM and migrations
- **AI Chat Integration**: Local Gemma:7B model integration via Ollama
- **CORS Support**: Cross-origin resource sharing enabled
- **Docker Support**: Containerized application and database
- **Testing**: Comprehensive test suite with pytest
- **Code Quality**: Structured with services, models, and blueprints
- **Swagger Documentation**: Interactive API documentation

## 📋 Prerequisites

- Python 3.10+
- Poetry (Python dependency manager) or pip
- Docker & Docker Compose
- MySQL (or use Docker MySQL container)
- **Ollama** (for AI chat functionality)
- **Gemma:7B model** (downloaded via Ollama)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd hackatlon-back
```

### 2. Install Dependencies

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

### 3. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit the .env file with your configuration
nano .env
```

### 4. AI Chat Setup (Optional but Recommended)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Download Gemma:7B model
ollama pull gemma:7b

# Verify installation
ollama list
```

### 5. Database Setup

#### Option A: Using Docker (Recommended)

```bash
# Start MySQL container
docker-compose up -d mysql

# The database will be automatically created and initialized
```

#### Option B: Local MySQL

```bash
# Make sure MySQL is running and create the database
mysql -u root -p
CREATE DATABASE hackatlon_db;
```

## 🚀 Running the Application

### Development Mode

```bash
# Method 1: Using Poetry
poetry run python app/main.py

# Method 2: Using the run script
poetry run python run.py
```

### Docker

```bash
# Build the image
docker build -t hackatlon-backend .

# Run the container
docker run -p 8000:8000 hackatlon-backend

# Or use docker-compose for full stack
docker-compose up --build
```

## 📚 API Endpoints

### Health Check

- **GET** `/` - Root endpoint
- **GET** `/health` - Health check endpoint

### AI Chat (NEW! 🤖)

- **POST** `/chat` - Send a query to Gemma:7B model
  ```json
  {
    "query": "Explícame qué es la inteligencia artificial"
  }
  ```
- **GET** `/chat/model-info` - Get information about the current model

### Authentication

## 🧪 Testing

### Run All Tests

```bash
poetry run pytest
```

### Run Specific Tests

```bash
# Health check tests
poetry run pytest test/test_health.py -v

# Docker tests
poetry run pytest test/test_docker.py -v
```

### Test Chat Endpoint

```bash
# Run comprehensive chat API tests
python test_chat.py

# Or test manually with curl
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hola, ¿cómo estás?"}'
```

## 🐳 Docker Configuration

### MySQL Database

The `docker-compose.yml` includes:
- MySQL 8.0 database
- phpMyAdmin for database management (http://localhost:8080)
- Persistent data volumes
- Network configuration

### Environment Variables

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/hackatlon_db

# Flask Configuration
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=1

# MySQL Configuration (for Docker)
MYSQL_ROOT_PASSWORD=password
MYSQL_DATABASE=hackatlon_db
MYSQL_USER=hackuser
MYSQL_PASSWORD=hackpass
```

## 📁 Project Structure

```
hackatlon-back/
├── app/
│   ├── main.py                  # Application entry point
│   ├── routes/
│   │   └── health_controller.py # Health check routes
│   └── services/
│       └── health_service.py    # Health check business logic
├── test/
│   ├── test_health.py           # Health endpoint tests
│   └── test_docker.py           # Docker integration tests
├── docker-compose.yml           # Docker services configuration
├── Dockerfile                   # Application container
├── pyproject.toml              # Poetry dependencies
├── .env.example                # Environment template
└── README.md                   # This file
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check if MySQL is running
   docker-compose ps
   
   # Restart MySQL container
   docker-compose restart mysql
   ```

2. **Poetry Dependencies**
   ```bash
   # Update lock file
   poetry lock --no-update
   
   # Reinstall dependencies
   poetry install
   ```

3. **Port Already in Use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   
   # Kill process
   kill -9 <PID>
   ```

4. **Chat/Ollama Issues**
   ```bash
   # Check if Ollama is running
   ollama list
   
   # Restart Ollama service
   sudo systemctl restart ollama
   
   # Check if model is available
   ollama run gemma:7b "test"
   ```

## 🤖 AI Chat Documentation

For detailed information about the chat API, including integration examples and troubleshooting, see [CHAT_API_DOCS.md](./CHAT_API_DOCS.md).

## 👥 Authors

- **MikeChamp4** - *Initial work* - zambranocmiguele@gmail.com

---

**Happy Coding! 🚀**
