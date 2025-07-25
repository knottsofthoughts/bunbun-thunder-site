import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.engine import CoreEngine
from features.file_integrity import FileIntegrityMonitor, get_file_hash

class TestFileIntegrity(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_knowledge_base.db"
        self.engine = CoreEngine(db_path=self.db_path)
        self.monitor = FileIntegrityMonitor(self.engine)
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as f:
            f.write("This is a test file.")

    def tearDown(self):
        self.engine.conn.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_monitor_file(self):
        self.monitor.monitor_file(self.test_file)
        events = self.engine.get_events_by_type("file_integrity_check")
        self.assertEqual(len(events), 1)

    def test_check_for_suspicious_modification(self):
        initial_hash = get_file_hash(self.test_file)
        self.monitor.monitor_file(self.test_file)
        with open(self.test_file, "w") as f:
            f.write("This file has been modified.")
        self.monitor.monitor_file(self.test_file)
        events = self.engine.get_events_by_type("suspicious_file_modification")
        self.assertEqual(len(events), 1)

    def test_check_for_known_good_modification(self):
        initial_hash = get_file_hash(self.test_file)
        self.monitor.monitor_file(self.test_file)
        # Add the new hash to the whitelist
        with open(self.test_file, "w") as f:
            f.write("This is a known good modification.")
        new_hash = get_file_hash(self.test_file)
        self.monitor.known_good_hashes[new_hash] = self.test_file
        self.monitor.monitor_file(self.test_file)
        events = self.engine.get_events_by_type("file_modified")
        self.assertEqual(len(events), 1)

if __name__ == '__main__':
    unittest.main()
