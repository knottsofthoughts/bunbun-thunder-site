import unittest
import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cybersecurity_app.core.engine import CoreEngine

class TestEngine(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_knowledge_base.db"
        self.engine = CoreEngine(db_path=self.db_path)
        cursor = self.engine.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                event_data TEXT NOT NULL,
                event_type TEXT NOT NULL
            )
        """)
        self.engine.conn.commit()

    def tearDown(self):
        self.engine.conn.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_learn_from_event(self):
        event = {"type": "test_event", "data": "some_data"}
        self.engine.process_event(event)
        cursor = self.engine.conn.cursor()
        cursor.execute("SELECT * FROM events WHERE event_type = 'test_event'")
        events = cursor.fetchall()
        self.assertEqual(len(events), 1)
        self.assertEqual(json.loads(events[0][2])["data"], "some_data")
        # Cleanup
        cursor.execute("DELETE FROM events WHERE event_type = 'test_event'")
        self.engine.conn.commit()

if __name__ == '__main__':
    unittest.main()
