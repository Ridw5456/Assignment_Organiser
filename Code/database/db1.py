import sqlite3

con = sqlite3.connect("db.db")
cur = con.cursor()

con.execute("""CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY,
username TEXT, password TEXT, security_code TEXT)""")

con.execute("""CREATE TABLE IF NOT EXISTS sessions(session_id INTEGER PRIMARY KEY,
start_time TEXT, end_time TEXT, score INTEGER, user_id TEXT,
FOREIGN KEY(user_id) REFERENCES users(user_id))""")

con.execute("""CREATE TABLE IF NOT EXISTS timetables(timetable_id TEXT PRIMARY KEY,
path TEXT, user_id TEXT, FOREIGN KEY(user_id) REFERENCES users(user_id))""")

cur.execute("INSERT INTO users VALUES(000, 'testuser', 'password', '0000')")

con.commit()
cur.execute("SELECT * FROM users")

res = cur.fetchall()
print(res)
con.close
