from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import sqlite3, json, datetime
BASE=Path(__file__).resolve().parent; DB=BASE/'data'/'easycommunity.db'; CONFIG=json.loads((BASE/'config'/'app_config.json').read_text())
app=FastAPI(title='EasyCommunity API',version=CONFIG['version'])
class Decision(BaseModel): decision:str; reason:str=''
def conn():
    DB.parent.mkdir(exist_ok=True); c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init_db():
    c=conn(); c.executescript('''
    CREATE TABLE IF NOT EXISTS listings(id INTEGER PRIMARY KEY,name TEXT,category TEXT,description TEXT,area TEXT,accessibility TEXT,verified INTEGER,parkeasy_supported INTEGER);
    CREATE TABLE IF NOT EXISTS notices(id INTEGER PRIMARY KEY,title TEXT,body TEXT,area TEXT,source TEXT,evidence_status TEXT,confidence TEXT,effective_from TEXT,effective_to TEXT);
    CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,title TEXT,event_type TEXT,impact_window TEXT,area TEXT,summary TEXT,source TEXT,confidence TEXT,status TEXT);
    CREATE TABLE IF NOT EXISTS recommendations(id INTEGER PRIMARY KEY,title TEXT,reason TEXT,priority TEXT,evidence TEXT,confidence TEXT,status TEXT,decision_reason TEXT,updated_at TEXT);
    CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY,entity_type TEXT,entity_id INTEGER,action TEXT,evidence TEXT,created_at TEXT);
    ''')
    if c.execute('SELECT COUNT(*) n FROM listings').fetchone()['n']==0:
        seed=json.loads((BASE/'config'/'seed_data.json').read_text())
        for x in seed['listings']: c.execute('INSERT INTO listings(name,category,description,area,accessibility,verified,parkeasy_supported) VALUES(?,?,?,?,?,?,?)',tuple(x.values()))
        for x in seed['notices']: c.execute('INSERT INTO notices(title,body,area,source,evidence_status,confidence,effective_from,effective_to) VALUES(?,?,?,?,?,?,?,?)',tuple(x.values()))
        for x in seed['events']: c.execute('INSERT INTO events(title,event_type,impact_window,area,summary,source,confidence,status) VALUES(?,?,?,?,?,?,?,?)',tuple(x.values()))
        for x in seed['recommendations']: c.execute('INSERT INTO recommendations(title,reason,priority,evidence,confidence,status) VALUES(?,?,?,?,?,?)',tuple(x.values()))
    c.commit(); c.close()
init_db()
app.mount('/static',StaticFiles(directory=BASE/'static'),name='static')
@app.get('/')
def home(): return FileResponse(BASE/'static'/'index.html')
@app.get('/admin')
def admin(): return FileResponse(BASE/'static'/'admin.html')
@app.get('/manifest.webmanifest')
def manifest(): return FileResponse(BASE/'static'/'manifest.webmanifest',media_type='application/manifest+json')
@app.get('/api/health')
def health(): return {'product':CONFIG['product'],'version':CONFIG['version'],'status':'live','data_state':'live','checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
@app.get('/api/listings')
def listings(q:str='',category:str=''):
    c=conn(); sql='SELECT * FROM listings WHERE 1=1'; p=[]
    if q: sql+=' AND (name LIKE ? OR description LIKE ? OR area LIKE ?)'; p += [f'%{q}%']*3
    if category: sql+=' AND category=?'; p.append(category)
    rows=[dict(r) for r in c.execute(sql+' ORDER BY verified DESC,name',p)];c.close();return rows
@app.get('/api/notices')
def notices():
    c=conn();r=[dict(x) for x in c.execute('SELECT * FROM notices ORDER BY effective_from')];c.close();return r
@app.get('/api/events')
def events():
    c=conn();r=[dict(x) for x in c.execute('SELECT * FROM events ORDER BY id DESC')];c.close();return r
@app.get('/api/recommendations')
def recommendations():
    c=conn();r=[dict(x) for x in c.execute('SELECT * FROM recommendations ORDER BY CASE priority WHEN "P1" THEN 1 WHEN "P2" THEN 2 WHEN "P3" THEN 3 ELSE 4 END,id')];c.close();return r
@app.post('/api/recommendations/{rid}/decision')
def decide(rid:int,d:Decision):
    allowed={'Approved','Rejected','Deferred','Modified','Review Requested'}
    if d.decision not in allowed: raise HTTPException(400,'Unsupported decision')
    c=conn(); row=c.execute('SELECT id FROM recommendations WHERE id=?',(rid,)).fetchone()
    if not row: c.close(); raise HTTPException(404,'Recommendation not found')
    now=datetime.datetime.now(datetime.timezone.utc).isoformat();c.execute('UPDATE recommendations SET status=?,decision_reason=?,updated_at=? WHERE id=?',(d.decision,d.reason,now,rid));c.execute('INSERT INTO audit(entity_type,entity_id,action,evidence,created_at) VALUES(?,?,?,?,?)',('recommendation',rid,d.decision,d.reason,now));c.commit();c.close();return {'id':rid,'status':d.decision,'updated_at':now}
@app.get('/api/audit')
def audit():
    c=conn();r=[dict(x) for x in c.execute('SELECT * FROM audit ORDER BY id DESC LIMIT 100')];c.close();return r
