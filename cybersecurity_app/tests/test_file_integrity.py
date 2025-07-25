import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.engine import CoreEngine
from features.file_integrity import FileIntegrityMonitor, get_file_hash

class TestFileIntegrity(unittest.TestCase):

    def setUp(self):
        self.engine = CoreEngine(knowledge_base_path="test_knowledge_base.json")
        self.monitor = FileIntegrityMonitor(self.engine)
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as f:
            f.write("This is a test file.")

    def tearDown(self):
        if os.path.exists("test_knowledge_base.json"):
            os.remove("test_knowledge_base.json")
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_monitor_file(self):
        self.monitor.monitor_file(self.test_file)
        self.assertIn("file_integrity_check", self.engine.knowledge_base)
        self.assertEqual(len(self.engine.knowledge_base["file_integrity_check"]["events"]), 1)

    def test_check_for_modification(self):
        initial_hash = get_file_hash(self.test_file)
        self.monitor.monitor_file(self.test_file)
        with open(self.test_file, "w") as f:
            f.write("This file has been modified.")
        self.monitor.monitor_file(self.test_file)
        self.assertIn("file_modified", self.engine.knowledge_base)
        self.assertEqual(len(self.engine.knowledge_base["file_modified"]["events"]), 1)

if __name__ == '__main__':
    unittest.main()
