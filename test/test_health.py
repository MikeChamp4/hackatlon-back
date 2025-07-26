import pytest
from app.main import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'Working'
    assert 'message' in data
    assert 'timestamp' in data
    assert 'version' in data

def test_root_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'Working'
    assert data['message'] == 'Flask API is running!'
    assert data['version'] == '1.0.0'
