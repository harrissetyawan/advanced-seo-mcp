import sqlite3
import json
import time
from typing import Optional, Dict, Any, Tuple
from pathlib import Path

DB_PATH = Path.home() / ".advanced_seo_mcp_cache.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS signatures (
            domain TEXT PRIMARY KEY,
            signature TEXT,
            valid_until TEXT,
            overview_data TEXT,
            timestamp REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_signature(domain: str, signature: str, valid_until: str, overview_data: Dict[str, Any]):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO signatures (domain, signature, valid_until, overview_data, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (domain, signature, valid_until, json.dumps(overview_data), time.time()))
    conn.commit()
    conn.close()

def get_signature(domain: str) -> Tuple[Optional[str], Optional[str], Optional[Dict[str, Any]]]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT signature, valid_until, overview_data FROM signatures WHERE domain = ?', (domain,))
    row = c.fetchone()
    conn.close()
    
    if row:
        signature, valid_until, overview_data_json = row
        try:
            overview_data = json.loads(overview_data_json)
        except:
            overview_data = {}
        return signature, valid_until, overview_data
    return None, None, None
