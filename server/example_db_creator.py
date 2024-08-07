import sqlite3
import hashlib

conn = sqlite3.connect("server/userdata.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    status INTEGER DEFAULT 0,
    privilege_level INTEGER DEFAULT 0
)
""")

username1, password1 = "a", hashlib.sha256("a1".encode("utf-8")).hexdigest()
username2, password2 = "b", hashlib.sha256("b2".encode("utf-8")).hexdigest()
username3, password3 = "c", hashlib.sha256("c3".encode("utf-8")).hexdigest()

cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username1, password1))
cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username2, password2))
cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username3, password3))

conn.commit()