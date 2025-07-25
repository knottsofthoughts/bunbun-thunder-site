import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.engine import CoreEngine

class TestEngine(unittest.TestCase):

    def setUp(self):
        self.engine = CoreEngine(knowledge_base_path="test_knowledge_base.json")

    def tearDown(self):
        if os.path.exists("test_knowledge_base.json"):
            os.remove("test_knowledge_base.json")

    def test_learn_from_event(self):
        event = {"type": "test_event", "data": "some_data"}
        self.engine.process_event(event)
        self.assertIn("test_event", self.engine.knowledge_base)
        self.assertEqual(self.engine.knowledge_base["test_event"]["count"], 1)
        self.assertEqual(len(self.engine.knowledge_base["test_event"]["events"]), 1)

if __name__ == '__main__':
    unittest.main()
