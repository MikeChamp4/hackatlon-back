# Hackatlon Backend - Flask API

A robust Flask-based REST API with MySQL database integration, designed for hackathon projects.

## 🚀 Features

- **Flask Framework**: Modern Python web framework
- **MySQL Database**: With SQLAlchemy ORM and migrations
- **CORS Support**: Cross-origin resource sharing enabled
- **Docker Support**: Containerized application and database
- **Testing**: Comprehensive test suite with pytest
- **Code Quality**: Structured with services, models, and blueprints

## 📋 Prerequisites

- Python 3.10+
- Poetry (Python dependency manager)
- Docker & Docker Compose
- MySQL (or use Docker MySQL container)

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

### 4. Database Setup

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

## 👥 Authors

- **MikeChamp4** - *Initial work* - zambranocmiguele@gmail.com

---

**Happy Coding! 🚀**
