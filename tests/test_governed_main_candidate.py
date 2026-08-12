from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import app


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def governed_client(tmp_path, monkeypatch):
    monkeypatch.setattr(app, "DB", tmp_path / "easycommunity-governed-test.db")
    app.init_db()
    return TestClient(app.app)


def test_governed_health_and_listings_work(governed_client):
    health = governed_client.get("/api/health")
    assert health.status_code == 200
    payload = health.json()
    assert payload["product"] == "EasyCommunity"
    assert payload["status"] == "live"
    assert payload["data_state"] == "live"

    listings = governed_client.get("/api/listings")
    assert listings.status_code == 200
    assert isinstance(listings.json(), list)
    assert listings.json()


def test_zero_result_search_has_explicit_empty_state(governed_client):
    response = governed_client.get(
        "/api/listings", params={"q": "__no_such_easycommunity_item__"}
    )
    assert response.status_code == 200
    assert response.json() == []

    js = (ROOT / "static" / "community.js").read_text(encoding="utf-8")
    assert "No matching entries." in js


def test_actual_governed_navigation_is_wired():
    html = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
    common = (ROOT / "static" / "common.js").read_text(encoding="utf-8")

    for view in ["discover", "notices", "events", "saved"]:
        assert f'data-view="{view}"' in html
        assert f'id="{view}"' in html
    assert "$$('[data-view]').forEach" in common
    assert "activateView(b.dataset.view)" in common


def test_obsolete_prototype_controls_remain_absent():
    html = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
    community = (ROOT / "static" / "community.js").read_text(encoding="utf-8")
    common = (ROOT / "static" / "common.js").read_text(encoding="utf-8")
    combined = html + "\n" + community + "\n" + common

    for obsolete_marker in [
        "btnMenu",
        "Messages feature coming soon",
        "View all alerts",
        "Alert chevron",
        "Plan ▾",
        "refreshDividers",
        "notif-badge",
        "Water Supply Restored",
    ]:
        assert obsolete_marker not in combined


def test_candidate_uses_fastapi_backend_and_api_driven_content():
    app_source = (ROOT / "app.py").read_text(encoding="utf-8")
    community = (ROOT / "static" / "community.js").read_text(encoding="utf-8")

    assert "from fastapi import FastAPI" in app_source
    assert "app = FastAPI(" in app_source
    assert "@app.get('/api/listings')" in app_source
    assert "@app.get('/api/notices')" in app_source
    assert "@app.get('/api/events')" in app_source
    assert "api('/api/listings" in community
    assert "api('/api/notices')" in community
    assert "api('/api/events')" in community
    assert "const ALERTS" not in community
    assert "const PLANS" not in community


def test_static_client_escapes_api_content():
    community = (ROOT / "static" / "community.js").read_text(encoding="utf-8")
    common = (ROOT / "static" / "common.js").read_text(encoding="utf-8")

    assert "esc(r.name)" in community
    assert "esc(r.description)" in community
    assert "function esc" in common


def test_current_main_truthfulness_controls_are_preserved():
    app_source = (ROOT / "app.py").read_text(encoding="utf-8")

    assert "data_freshness_minutes" in app_source
    assert "data_state = 'live' if age_minutes <= CONFIG['data_freshness_minutes'] else 'stale'" in app_source
    assert "raise HTTPException(status_code=503, detail='Database unavailable')" in app_source
    assert "escape_like" in app_source
