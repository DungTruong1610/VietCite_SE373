from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.security import reset_auth_service

QUESTION = "Một shop bán 2.400.000đ mỗi ngày, 30 ngày thì doanh thu bao nhiêu?"


@pytest.fixture
def client(monkeypatch) -> TestClient:
    monkeypatch.setenv("SEED_EDITOR_PASSWORD", "editor-pass-for-tests")
    monkeypatch.setenv("SEED_APPROVER_PASSWORD", "approver-pass-for-tests")
    monkeypatch.setenv("JWT_SECRET", "test-secret-" + "x" * 32)
    reset_auth_service()
    yield TestClient(app)
    reset_auth_service()


def _token(client: TestClient, user: str = "editor", password: str = "editor-pass-for-tests") -> str:
    r = client.post("/api/auth/login", json={"username": user, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_health_exposes_flags_not_keys(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok" and body["features"] == {"deepseek": False, "jina": False, "gemini": False}
    assert r.headers["X-Content-Type-Options"] == "nosniff"


def test_login_not_configured_returns_503(monkeypatch):
    monkeypatch.setenv("SEED_EDITOR_PASSWORD", "")
    monkeypatch.setenv("SEED_APPROVER_PASSWORD", "")
    reset_auth_service()
    r = TestClient(app).post("/api/auth/login", json={"username": "editor", "password": "x"})
    assert r.status_code == 503 and "SEED_EDITOR_PASSWORD" in r.json()["detail"]
    reset_auth_service()


def test_login_me_and_wrong_password(client):
    token = _token(client, "approver", "approver-pass-for-tests")
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.json() == {"username": "approver", "role": "approver"}
    assert client.post("/api/auth/login", json={"username": "editor", "password": "nope"}).status_code == 401
    assert client.get("/api/auth/me", headers={"Authorization": "Bearer garbage"}).status_code == 401


def test_login_locks_after_repeated_failures(client):
    for _ in range(5):
        client.post("/api/auth/login", json={"username": "editor", "password": "bad"})
    locked = client.post("/api/auth/login", json={"username": "editor", "password": "editor-pass-for-tests"})
    assert locked.status_code == 401


def test_demo_stream_requires_auth(client):
    assert client.get("/api/runs/demo/stream", params={"question": QUESTION}).status_code == 401


def test_live_mode_refused_without_key(client):
    token = _token(client)
    r = client.get(
        "/api/runs/demo/stream",
        params={"question": QUESTION, "mode": "live"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 400


def test_demo_stream_emits_trace_then_done(client):
    token = _token(client)
    events = []
    with client.stream(
        "GET",
        "/api/runs/demo/stream",
        params={"question": QUESTION, "mode": "mock"},
        headers={"Authorization": f"Bearer {token}"},
    ) as r:
        assert r.status_code == 200
        current = None
        for line in r.iter_lines():
            if line.startswith("event:"):
                current = line.split(":", 1)[1].strip()
            elif line.startswith("data:") and current:
                events.append((current, json.loads(line.split(":", 1)[1].strip())))
    kinds = [k for k, _ in events]
    assert kinds[-1] == "done" and kinds.count("trace") >= 4
    done = events[-1][1]
    assert done["stop_reason"] == "GOAL" and "72.000.000" in done["answer"]
    seqs = [d["seq"] for k, d in events if k == "trace"]
    assert seqs == sorted(seqs)
