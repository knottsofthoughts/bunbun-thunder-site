import hashlib
import os
from .threat_response import ThreatResponder

import hashlib
from .threat_response import ThreatResponder

class FileIntegrityMonitor:
    def __init__(self, engine):
        self.engine = engine
        self.responder = ThreatResponder(engine)
        self.hashes = {}

    def get_file_hash(self, filepath):
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    def monitor_file(self, filepath):
        if not os.path.exists(filepath):
            return
        file_hash = self.get_file_hash(filepath)
        if filepath in self.hashes:
            self.check_for_modification(filepath, file_hash)
        else:
            self.hashes[filepath] = file_hash
        event = {
            "type": "file_integrity_check",
            "filepath": filepath,
            "hash": file_hash
        }
        self.engine.process_event(event)

    def check_for_modification(self, filepath, current_hash):
        previous_hash = self.hashes[filepath]
        if current_hash != previous_hash:
            # Check against known good hashes
            known_good_hashes = [e["hash"] for e in self.engine.get_events_by_type("file_integrity_check") if e["filepath"] == filepath]
            if previous_hash in known_good_hashes:
                print(f"File has been modified (known good): {filepath}")
                modification_event = {
                    "type": "file_modified",
                    "filepath": filepath,
                    "previous_hash": previous_hash,
                    "current_hash": current_hash
                }
                self.engine.process_event(modification_event)
            else:
                print(f"Suspicious modification detected: {filepath}")
                modification_event = {
                    "type": "suspicious_file_modification",
                    "filepath": filepath,
                    "previous_hash": previous_hash,
                    "current_hash": current_hash
                }
                self.responder.respond_to_threat(modification_event)
        self.hashes[filepath] = current_hash
