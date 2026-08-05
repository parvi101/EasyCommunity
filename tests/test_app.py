import os,sys,tempfile
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from fastapi.testclient import TestClient
import app
client=TestClient(app.app)
def test_health():
    r=client.get('/api/health');assert r.status_code==200;assert r.json()['status']=='live'
def test_listings_and_search():
    assert len(client.get('/api/listings').json())>=4
    assert client.get('/api/listings?q=mall').json()[0]['parkeasy_supported']==1
def test_recommendation_decision_and_audit():
    recs=client.get('/api/recommendations').json();rid=recs[0]['id']
    r=client.post(f'/api/recommendations/{rid}/decision',json={'decision':'Approved','reason':'test evidence'});assert r.status_code==200
    assert any(x['entity_id']==rid for x in client.get('/api/audit').json())
def test_pwa_assets():
    assert client.get('/manifest.webmanifest').status_code==200
    assert client.get('/static/sw.js').status_code==200
