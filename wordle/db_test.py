import sqlite3

# Connect to the database (creates the file if it does not exist)
conn = sqlite3.connect('wordle_test.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL)
''')
conn.commit()

# Insert a row
cursor.execute("INSERT INTO games (name, score) VALUES (?, ?)", ("Erik", 1))
conn.commit()

# Querying
cursor.execute("Select * FROM games where ID = ?", (1,))
row = cursor.fetchall()

for line in row:
    print(line)

conn.close()