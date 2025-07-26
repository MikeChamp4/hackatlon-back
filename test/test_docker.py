import requests
from testcontainers.generic import ServerContainer
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.core.image import DockerImage

def test_docker_run():
    with DockerImage(path=".", tag="flask-test:latest") as image:
        with ServerContainer(port=8000, image=image) as flask_server:
            wait_for_logs(flask_server, "Running on http://0.0.0.0:8000")
            flask_server.get_api_url = lambda: flask_server._create_connection_url()
            print(f"API URL: {flask_server.get_api_url()}")
            
            # Test health endpoint
            response = requests.get(f"{flask_server.get_api_url()}/health")
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'Working'
            
            # Test root endpoint
            response = requests.get(f"{flask_server.get_api_url()}/")
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'Working'
