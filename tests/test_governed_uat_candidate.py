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
    js = (ROOT / 'static' / 'community.js').read_text(encoding='utf-8')
    combined = html + '\n' + js

    for obsolete_marker in [
        'btnMenu',
        'Messages feature coming soon',
        'View all alerts',
        'Alert chevron',
        'Plan ▾',
    ]:
        assert obsolete_marker not in combined


def test_static_client_javascript_escapes_api_content():
    community = (ROOT / 'static' / 'community.js').read_text(encoding='utf-8')
    common = (ROOT / 'static' / 'common.js').read_text(encoding='utf-8')
    assert 'esc(r.name)' in community
    assert 'esc(r.description)' in community
    assert 'function esc' in common
