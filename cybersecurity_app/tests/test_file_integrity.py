import unittest
import os
import shutil
from cybersecurity_app.core.engine import CoreEngine
from cybersecurity_app.features.file_integrity import FileIntegrityMonitor
from cybersecurity_app.features.threat_response import ThreatResponder

class TestFileIntegrity(unittest.TestCase):

    def setUp(self):
        self.engine = CoreEngine()
        self.monitor = FileIntegrityMonitor(self.engine)
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as f:
            f.write("This is a test file.")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists("quarantine"):
            shutil.rmtree("quarantine")

    def test_monitor_file(self):
        self.monitor.monitor_file(self.test_file)
        events = self.engine.get_events_by_type("file_integrity_check")
        self.assertGreaterEqual(len(events), 1)

    def test_check_for_suspicious_modification(self):
        self.monitor.monitor_file(self.test_file)
        with open(self.test_file, "w") as f:
            f.write("This is a malicious modification.")
        self.monitor.monitor_file(self.test_file)
        events = self.engine.get_events_by_type("suspicious_file_modification")
        self.assertEqual(len(events), 1)

    def test_check_for_known_good_modification(self):
        self.monitor.monitor_file(self.test_file)
        with open(self.test_file, "w") as f:
            f.write("This is a good modification.")
        # This hash should be added to a known good list in a real scenario
        self.monitor.monitor_file(self.test_file)
        events = self.engine.get_events_by_type("file_modified")
        self.assertGreaterEqual(len(events), 1)

if __name__ == '__main__':
    unittest.main()
