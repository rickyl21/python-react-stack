import sqlite3

# One file, no server. Delete dev.db to reset all data.
# check_same_thread=False: FastAPI runs sync routes in a thread pool.
db = sqlite3.connect("dev.db", check_same_thread=False)
db.row_factory = sqlite3.Row
db.execute("PRAGMA journal_mode = WAL")
db.execute("PRAGMA foreign_keys = ON")

# Schema lives here. CREATE TABLE IF NOT EXISTS keeps restarts safe.
db.executescript("""
CREATE TABLE IF NOT EXISTS items (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT    NOT NULL,
  created_at INTEGER NOT NULL
);
""")
db.commit()
