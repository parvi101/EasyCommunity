from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from pathlib import Path
from zoneinfo import ZoneInfo
import sqlite3, json, datetime

BASE = Path(__file__).resolve().parent
DB = BASE / 'data' / 'easycommunity.db'
CONFIG = json.loads((BASE / 'config' / 'app_config.json').read_text())
LOCAL_TZ = ZoneInfo(CONFIG.get('timezone', 'UTC'))
app = FastAPI(title='EasyCommunity API', version=CONFIG['version'])

class Decision(BaseModel):
    decision: str = Field(min_length=1, max_length=40)
    reason: str = Field(default='', max_length=2000)

def utcnow():
    return datetime.datetime.now(datetime.timezone.utc)

def local_now():
    return utcnow().astimezone(LOCAL_TZ)

def parse_local_timestamp(value):
    if not value:
        return None
    dt = datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=LOCAL_TZ)
    return dt.astimezone(LOCAL_TZ)

def conn():
    DB.parent.mkdir(exist_ok=True)
    c = sqlite3.connect(DB, timeout=5)
    c.row_factory = sqlite3.Row
    return c

def set_meta(c, key, value):
    c.execute('INSERT INTO metadata(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value', (key, value))

def get_meta(c, key):
    row = c.execute('SELECT value FROM metadata WHERE key=?', (key,)).fetchone()
    return row['value'] if row else None

def ensure_column(c, table, column, definition):
    columns = {row['name'] for row in c.execute(f'PRAGMA table_info({table})')}
    if column not in columns:
        c.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition}')

def init_db():
    c = conn()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS listings(id INTEGER PRIMARY KEY,name TEXT,category TEXT,description TEXT,area TEXT,accessibility TEXT,verified INTEGER,parkeasy_supported INTEGER);
    CREATE TABLE IF NOT EXISTS notices(id INTEGER PRIMARY KEY,title TEXT,body TEXT,area TEXT,source TEXT,evidence_status TEXT,confidence TEXT,effective_from TEXT,effective_to TEXT);
    CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,title TEXT,event_type TEXT,impact_window TEXT,area TEXT,summary TEXT,source TEXT,confidence TEXT,status TEXT,effective_from TEXT,effective_to TEXT);
    CREATE TABLE IF NOT EXISTS recommendations(id INTEGER PRIMARY KEY,title TEXT,reason TEXT,priority TEXT,evidence TEXT,confidence TEXT,status TEXT,decision_reason TEXT,updated_at TEXT);
    CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY,entity_type TEXT,entity_id INTEGER,action TEXT,evidence TEXT,created_at TEXT);
    CREATE TABLE IF NOT EXISTS metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL);
    ''')
    ensure_column(c, 'events', 'effective_from', 'TEXT')
    ensure_column(c, 'events', 'effective_to', 'TEXT')
    if c.execute('SELECT COUNT(*) n FROM listings').fetchone()['n'] == 0:
        seed = json.loads((BASE / 'config' / 'seed_data.json').read_text())
        for x in seed['listings']:
            c.execute('INSERT INTO listings(name,category,description,area,accessibility,verified,parkeasy_supported) VALUES(?,?,?,?,?,?,?)', tuple(x.values()))
        for x in seed['notices']:
            c.execute('INSERT INTO notices(title,body,area,source,evidence_status,confidence,effective_from,effective_to) VALUES(?,?,?,?,?,?,?,?)', tuple(x.values()))
        for x in seed['events']:
            c.execute('INSERT INTO events(title,event_type,impact_window,area,summary,source,confidence,status) VALUES(?,?,?,?,?,?,?,?)', tuple(x.values()))
        for x in seed['recommendations']:
            c.execute('INSERT INTO recommendations(title,reason,priority,evidence,confidence,status) VALUES(?,?,?,?,?,?)', tuple(x.values()))
        set_meta(c, 'data_refreshed_at', utcnow().isoformat())
    elif not get_meta(c, 'data_refreshed_at'):
        set_meta(c, 'data_refreshed_at', utcnow().isoformat())
    c.commit()
    c.close()

init_db()
app.mount('/static', StaticFiles(directory=BASE / 'static'), name='static')

@app.get('/')
def home():
    return FileResponse(BASE / 'static' / 'index.html')

@app.get('/admin')
def admin():
    return FileResponse(BASE / 'static' / 'admin.html')

@app.get('/manifest.webmanifest')
def manifest():
    return FileResponse(BASE / 'static' / 'manifest.webmanifest', media_type='application/manifest+json')

@app.get('/api/health')
def health():
    checked = utcnow()
    try:
        c = conn()
        c.execute('SELECT 1').fetchone()
        refreshed = get_meta(c, 'data_refreshed_at')
        listing_count = c.execute('SELECT COUNT(*) n FROM listings').fetchone()['n']
        c.close()
        if not refreshed or listing_count == 0:
            data_state = 'unavailable'
            age_minutes = None
        else:
            refreshed_dt = datetime.datetime.fromisoformat(refreshed.replace('Z', '+00:00'))
            if refreshed_dt.tzinfo is None:
                refreshed_dt = refreshed_dt.replace(tzinfo=datetime.timezone.utc)
            age_minutes = max(0, (checked - refreshed_dt.astimezone(datetime.timezone.utc)).total_seconds() / 60)
            data_state = 'live' if age_minutes <= CONFIG['data_freshness_minutes'] else 'stale'
        return {
            'product': CONFIG['product'], 'version': CONFIG['version'], 'status': 'live',
            'data_state': data_state, 'checked_at': checked.isoformat(),
            'data_refreshed_at': refreshed, 'freshness_age_minutes': round(age_minutes, 1) if age_minutes is not None else None,
            'freshness_threshold_minutes': CONFIG['data_freshness_minutes']
        }
    except sqlite3.Error as exc:
        raise HTTPException(status_code=503, detail='Database unavailable') from exc

def escape_like(value):
    return value.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')

@app.get('/api/listings')
def listings(q: str = Query(default='', max_length=200), category: str = Query(default='', max_length=100)):
    c = conn()
    sql = 'SELECT * FROM listings WHERE 1=1'
    p = []
    if q:
        pattern = f"%{escape_like(q)}%"
        sql += " AND (name LIKE ? ESCAPE '\\' OR description LIKE ? ESCAPE '\\' OR area LIKE ? ESCAPE '\\')"
        p += [pattern] * 3
    if category:
        sql += ' AND category=?'
        p.append(category)
    rows = [dict(r) for r in c.execute(sql + ' ORDER BY verified DESC,name', p)]
    c.close()
    return rows

@app.get('/api/notices')
def notices():
    now = local_now()
    c = conn()
    result = []
    for row in c.execute('SELECT * FROM notices ORDER BY effective_from'):
        item = dict(row)
        start = parse_local_timestamp(item.get('effective_from'))
        end = parse_local_timestamp(item.get('effective_to'))
        if end and end < now:
            continue
        item['temporal_state'] = 'upcoming' if start and start > now else 'current'
        result.append(item)
    c.close()
    return result

@app.get('/api/events')
def events():
    now = local_now()
    c = conn()
    rows = []
    for row in c.execute('SELECT * FROM events ORDER BY id DESC'):
        item = dict(row)
        start = parse_local_timestamp(item.get('effective_from'))
        end = parse_local_timestamp(item.get('effective_to'))
        if end and end < now:
            continue
        if not start and not end:
            item['temporal_state'] = 'timing-unverified'
        else:
            item['temporal_state'] = 'upcoming' if start and start > now else 'current'
        rows.append(item)
    c.close()
    return rows

@app.get('/api/recommendations')
def recommendations():
    c = conn()
    rows = [dict(x) for x in c.execute('SELECT * FROM recommendations ORDER BY CASE priority WHEN "P1" THEN 1 WHEN "P2" THEN 2 WHEN "P3" THEN 3 ELSE 4 END,id')]
    c.close()
    return rows

@app.post('/api/recommendations/{rid}/decision')
def decide(rid: int, d: Decision):
    allowed = {'Approved', 'Rejected', 'Deferred', 'Modified', 'Review Requested'}
    if d.decision not in allowed:
        raise HTTPException(400, 'Unsupported decision')
    c = conn()
    row = c.execute('SELECT id FROM recommendations WHERE id=?', (rid,)).fetchone()
    if not row:
        c.close()
        raise HTTPException(404, 'Recommendation not found')
    now = utcnow().isoformat()
    c.execute('UPDATE recommendations SET status=?,decision_reason=?,updated_at=? WHERE id=?', (d.decision, d.reason, now, rid))
    c.execute('INSERT INTO audit(entity_type,entity_id,action,evidence,created_at) VALUES(?,?,?,?,?)', ('recommendation', rid, d.decision, d.reason, now))
    c.commit()
    c.close()
    return {'id': rid, 'status': d.decision, 'updated_at': now}

@app.get('/api/audit')
def audit():
    c = conn()
    rows = [dict(x) for x in c.execute('SELECT * FROM audit ORDER BY id DESC LIMIT 100')]
    c.close()
    return rows
