from pathlib import Path

from fastapi.testclient import TestClient

from app import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def test_core_api_health_and_listings_work():
    health = client.get('/api/health')
    assert health.status_code == 200
    payload = health.json()
    assert payload['product'] == 'EasyCommunity'
    assert payload['status'] == 'live'

    listings = client.get('/api/listings')
    assert listings.status_code == 200
    assert isinstance(listings.json(), list)
    assert listings.json()


def test_zero_result_search_has_explicit_empty_state():
    response = client.get('/api/listings', params={'q': '__no_such_easycommunity_item__'})
    assert response.status_code == 200
    assert response.json() == []

    js = (ROOT / 'static' / 'community.js').read_text(encoding='utf-8')
    assert 'No matching entries.' in js


def test_actual_governed_navigation_is_wired():
    html = (ROOT / 'static' / 'index.html').read_text(encoding='utf-8')
    common = (ROOT / 'static' / 'common.js').read_text(encoding='utf-8')

    for view in ['discover', 'notices', 'events', 'saved']:
        assert f'data-view="{view}"' in html
        assert f'id="{view}"' in html
    assert "$$('[data-view]').forEach" in common
    assert 'activateView(b.dataset.view)' in common


def test_uat_report_obsolete_controls_are_not_in_governed_candidate():
    html = (ROOT / 'static' / 'index.html').read_text(encoding='utf-8')
    community = (ROOT / 'static' / 'community.js').read_text(encoding='utf-8')
    common = (ROOT / 'static' / 'common.js').read_text(encoding='utf-8')
    combined = html + '\n' + community + '\n' + common

    for obsolete_marker in [
        'btnMenu',
        'Messages feature coming soon',
        'View all alerts',
        'Alert chevron',
        'Plan ▾',
        'refreshDividers',
        'notif-badge',
        'Water Supply Restored',
    ]:
        assert obsolete_marker not in combined


def test_governed_candidate_uses_backend_api_not_hardcoded_alert_arrays():
    app_source = (ROOT / 'app.py').read_text(encoding='utf-8')
    community = (ROOT / 'static' / 'community.js').read_text(encoding='utf-8')

    assert "@app.get('/api/listings')" in app_source
    assert "@app.get('/api/notices')" in app_source
    assert "@app.get('/api/events')" in app_source
    assert "api('/api/listings" in community
    assert "api('/api/notices')" in community
    assert "api('/api/events')" in community
    assert 'const ALERTS' not in community
    assert 'const PLANS' not in community


def test_static_client_javascript_escapes_api_content():
    community = (ROOT / 'static' / 'community.js').read_text(encoding='utf-8')
    common = (ROOT / 'static' / 'common.js').read_text(encoding='utf-8')
    assert 'esc(r.name)' in community
    assert 'esc(r.description)' in community
    assert 'function esc' in common
