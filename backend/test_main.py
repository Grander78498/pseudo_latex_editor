from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_main():
    response = client.get('/')
    assert response.json().get('message') is not None


def test_get_expressions():
    response = client.get('/expressions')
    assert response.status_code == 200
    assert len(response.json()) != 0
