import platform

from app import app
from fastapi.testclient import TestClient


def test_health_version_and_python():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}
        body = client.get("/").json()
        assert body["version"] == "0.2.0" and body["python"] == platform.python_version()


def test_the_bake_trial_switch_fails_every_nth_page_request(monkeypatch):
    import app as module
    monkeypatch.setattr(module, "FAULT_EVERY", 2)
    with TestClient(app) as client:
        codes = [client.get("/").status_code for _ in range(4)]
        assert sorted(codes) == [200, 200, 500, 500] and client.get("/health").status_code == 200
