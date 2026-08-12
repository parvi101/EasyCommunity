import datetime, sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
import app

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(app, 'DB', tmp_path/'easycommunity.db')
    app.init_db()
    return TestClient(app.app)

def test_health_fresh_and_stale(client):
    fresh=client.get('/api/health'); assert fresh.status_code==200; assert fresh.json()['status']=='live'; assert fresh.json()['data_state']=='live'
    c=app.conn(); old=(app.utcnow()-datetime.timedelta(minutes=31)).isoformat(); app.set_meta(c,'data_refreshed_at',old); c.commit(); c.close()
    stale=client.get('/api/health'); assert stale.json()['status']=='live'; assert stale.json()['data_state']=='stale'

def test_health_unavailable_when_core_data_missing(client):
    c=app.conn(); c.execute('DELETE FROM listings'); c.commit(); c.close()
    assert client.get('/api/health').json()['data_state']=='unavailable'

def test_listings_and_literal_wildcard_search(client):
    assert len(client.get('/api/listings').json())>=4
    assert client.get('/api/listings?q=mall').json()[0]['parkeasy_supported']==1
    assert client.get('/api/listings?q=%25').json()==[]
    assert client.get('/api/listings?q=_').json()==[]

def test_query_length_limit(client):
    assert client.get('/api/listings?q='+'x'*201).status_code==422

def test_notice_expiry_is_enforced(client):
    c=app.conn(); c.execute('DELETE FROM notices')
    now=app.local_now()
    expired=(now-datetime.timedelta(hours=2)).replace(tzinfo=None).isoformat(); future=(now+datetime.timedelta(hours=2)).replace(tzinfo=None).isoformat(); start=(now-datetime.timedelta(hours=1)).replace(tzinfo=None).isoformat()
    c.execute('INSERT INTO notices(title,body,area,source,evidence_status,confidence,effective_from,effective_to) VALUES(?,?,?,?,?,?,?,?)',('expired','x','x','x','Verified','High',start,expired))
    c.execute('INSERT INTO notices(title,body,area,source,evidence_status,confidence,effective_from,effective_to) VALUES(?,?,?,?,?,?,?,?)',('active','x','x','x','Verified','High',start,future)); c.commit(); c.close()
    rows=client.get('/api/notices').json(); assert [x['title'] for x in rows]==['active']; assert rows[0]['temporal_state']=='current'

def test_event_expiry_and_legacy_timing_state(client):
    legacy=client.get('/api/events').json(); assert legacy; assert all(x['temporal_state']=='timing-unverified' for x in legacy)
    c=app.conn(); now=app.local_now(); expired=(now-datetime.timedelta(hours=1)).replace(tzinfo=None).isoformat(); start=(now-datetime.timedelta(hours=2)).replace(tzinfo=None).isoformat()
    c.execute('INSERT INTO events(title,event_type,impact_window,area,summary,source,confidence,status,effective_from,effective_to) VALUES(?,?,?,?,?,?,?,?,?,?)',('expired event','Test','Now','x','x','x','High','Confirmed',start,expired)); c.commit(); c.close()
    assert all(x['title']!='expired event' for x in client.get('/api/events').json())

def test_recommendation_decision_modified_and_audit(client):
    rid=client.get('/api/recommendations').json()[0]['id']
    r=client.post(f'/api/recommendations/{rid}/decision',json={'decision':'Modified','reason':'test evidence'}); assert r.status_code==200; assert r.json()['status']=='Modified'
    assert any(x['entity_id']==rid and x['action']=='Modified' for x in client.get('/api/audit').json())

def test_invalid_decision_rejected(client):
    rid=client.get('/api/recommendations').json()[0]['id']; assert client.post(f'/api/recommendations/{rid}/decision',json={'decision':'Anything','reason':''}).status_code==400

def test_decision_reason_length_limit(client):
    rid=client.get('/api/recommendations').json()[0]['id']; assert client.post(f'/api/recommendations/{rid}/decision',json={'decision':'Approved','reason':'x'*2001}).status_code==422

def test_pwa_assets_and_api_not_cached(client):
    assert client.get('/manifest.webmanifest').status_code==200; sw=client.get('/static/sw.js'); assert sw.status_code==200; assert "startsWith('/api/')" in sw.text

def test_admin_exposes_modified_action(client):
    js=client.get('/static/community_admin.js'); assert js.status_code==200; assert "'Modified'" in js.text
