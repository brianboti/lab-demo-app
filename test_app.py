import platform

from app import app
from fastapi.testclient import TestClient


def test_health_version_and_python():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}
        body = client.get("/").json()
        assert body["version"] == "0.2.0" and body["python"] == platform.python_version()
