import sqlite3
from datetime import datetime

class WordleDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('wordle_test2.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS games (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            score INTEGER NOT NULL,
                            difficulty INTEGER NOT NULL,
                            word_length INTEGER NOT NULL,
                            guesses INTEGER NOT NULL,
                            won INTEGER NOT NULL,
                            word TEXT NOT NULL,
                            date TEXT NOT NULL
                            )
                ''')
        self.conn.commit()

    def add_to_db(self, name, score, difficulty, word_length, guesses, won, word):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO games (name, score, difficulty, word_length, guesses, won, word, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (name, score, difficulty, word_length, guesses, won, word, date))
        self.conn.commit()
        print("Entry saved to database")

    def query_games(self):
        self.cursor.execute("SELECT * FROM games")
        return self.cursor.fetchall()

    def query_by_player(self, name):
        self.cursor.execute("SELECT * FROM games WHERE name = ?", (name,))
        return self.cursor.fetchall()

    def query_by_score(self, limit=10):
        self.cursor.execute("SELECT * FROM games ORDER BY score DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

def main():
    db = WordleDatabase()
    # db.add_to_db("Erik", 50, 2, 6, 4, True, "what")
    games = db.query_games()
    column_names = [description[0] for description in db.cursor.description]
    print(column_names)
    for game in games:
        print(game)
    db.close()


if __name__ == "__main__":
    main()
