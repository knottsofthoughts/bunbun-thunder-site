import sqlite3
import json

class CoreEngine:
    def __init__(self, db_path="knowledge_base.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                event_data TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def process_event(self, event):
        # Placeholder for event processing logic
        print(f"Processing event: {event}")
        self.learn_from_event(event)

    def learn_from_event(self, event):
        # More sophisticated learning logic will be added here
        print(f"Learning from event: {event}")
        event_type = event.get("type")
        if event_type:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO events (event_type, event_data) VALUES (?, ?)",
                           (event_type, json.dumps(event)))
            self.conn.commit()

    def get_events_by_type(self, event_type):
        cursor = self.conn.cursor()
        cursor.execute("SELECT event_data FROM events WHERE event_type = ?", (event_type,))
        return [json.loads(row[0]) for row in cursor.fetchall()]

    def __del__(self):
        self.conn.close()
