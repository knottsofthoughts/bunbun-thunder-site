import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.engine import CoreEngine

class TestEngine(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_knowledge_base.db"
        self.engine = CoreEngine(db_path=self.db_path)

    def tearDown(self):
        self.engine.conn.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_learn_from_event(self):
        event = {"type": "test_event", "data": "some_data"}
        self.engine.process_event(event)
        events = self.engine.get_events_by_type("test_event")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["data"], "some_data")

if __name__ == '__main__':
    unittest.main()
