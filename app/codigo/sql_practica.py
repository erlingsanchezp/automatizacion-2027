import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE eventos (event_id TEXT PRIMARY KEY, sede TEXT NOT NULL)")
con.execute("INSERT INTO eventos VALUES (?,?)", ("evt-001", "villaflora"))
try:
    con.execute("INSERT INTO eventos VALUES (?,?)", ("evt-001", "villaflora"))
except sqlite3.IntegrityError:
    print("Duplicado rechazado correctamente")
print(con.execute("SELECT sede,COUNT(*) FROM eventos GROUP BY sede").fetchall())
con.close()
