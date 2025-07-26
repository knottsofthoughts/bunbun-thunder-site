import unittest
import os
import shutil
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cybersecurity_app.core.engine import CoreEngine
from cybersecurity_app.features.threat_response import ThreatResponder

class TestThreatResponse(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_knowledge_base.db"
        self.engine = CoreEngine(db_path=self.db_path)
        self.responder = ThreatResponder(self.engine)
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as f:
            f.write("This is a test file.")
        self.quarantine_dir = "quarantine"
        if not os.path.exists(self.quarantine_dir):
            os.mkdir(self.quarantine_dir)

    def tearDown(self):
        self.engine.conn.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.quarantine_dir):
            shutil.rmtree(self.quarantine_dir)

    def test_quarantine_file(self):
        event = {
            "type": "suspicious_file_modification",
            "filepath": self.test_file
        }
        self.responder.respond_to_threat(event)
        quarantined_file_path = os.path.join(self.quarantine_dir, self.test_file)
        self.assertTrue(os.path.exists(quarantined_file_path))
        events = self.engine.get_events_by_type("file_quarantined")
        self.assertEqual(len(events), 1)

if __name__ == '__main__':
    unittest.main()
