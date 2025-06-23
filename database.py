import sqlite3

import sqlite3

def init_db():
    conn = sqlite3.connect('threats.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            threat_type TEXT,
            timestamp TEXT,
            severity TEXT,
            ip_address TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')
    conn.commit()
    conn.close()


def insert_threat(threat_type, timestamp, severity, ip_address, lat=None, lon=None):
    conn = sqlite3.connect('threats.db')
    c = conn.cursor()
    c.execute('INSERT INTO threats (threat_type, timestamp, severity, ip_address, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)',
              (threat_type, timestamp, severity, ip_address, lat, lon))
    conn.commit()
    conn.close()

def blacklist_ip(ip_address, reason):
    conn = sqlite3.connect('threats.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO blacklist (ip_address, reason) VALUES (?, ?)', (ip_address, reason))
    conn.commit()
    conn.close()
