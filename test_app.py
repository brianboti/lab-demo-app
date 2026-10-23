import html
import platform

from app import MESSAGE, VERSION, app
from fastapi.testclient import TestClient


def test_health_and_the_page_shows_the_message():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}
        page = client.get("/")
        assert page.status_code == 200 and page.headers["content-type"].startswith("text/html")
        assert f"<h1>{html.escape(MESSAGE)}</h1>" in page.text and f"version {VERSION}" in page.text
        body = client.get("/api").json()
        assert body["message"] == MESSAGE and body["version"] == VERSION and body["python"] == platform.python_version()


def test_the_message_is_escaped(monkeypatch):
    import app as module
    monkeypatch.setattr(module, "MESSAGE", "<script>alert(1)</script>")
    with TestClient(app) as client:
        text = client.get("/").text
        assert "<script>alert(1)</script>" not in text and "&lt;script&gt;" in text


def test_the_bake_trial_switch_fails_every_nth_page_request(monkeypatch):
    import app as module
    monkeypatch.setattr(module, "FAULT_EVERY", 2)
    with TestClient(app) as client:
        codes = [client.get("/").status_code for _ in range(4)]
        assert sorted(codes) == [200, 200, 500, 500] and client.get("/health").status_code == 200
