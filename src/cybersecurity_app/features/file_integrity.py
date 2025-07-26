import hashlib
import os
from cybersecurity_app.features.threat_response import ThreatResponder

def get_file_hash(filepath):
    """Calculates the SHA256 hash of a file."""
    if not os.path.exists(filepath):
        return None
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

class FileIntegrityMonitor:
    def __init__(self, engine):
        self.engine = engine
        self.responder = ThreatResponder(engine)
        self.known_good_hashes = {
            "f29bc64a9d3732b4b9035125fdb3285f5b6455778edca72414671e0ca3b2e0de": "test_file.txt"
        }

    def monitor_file(self, filepath):
        """Monitors a file for changes."""
        file_hash = get_file_hash(filepath)
        if file_hash:
            event = {
                "type": "file_integrity_check",
                "filepath": filepath,
                "hash": file_hash
            }
            self.engine.process_event(event)
            self.check_for_modification(filepath, file_hash)

    def check_for_modification(self, filepath, current_hash):
        """Checks if a file has been modified."""
        events = self.engine.get_events_by_type("file_integrity_check")
        for event in events:
            if event["filepath"] == filepath and event["hash"] != current_hash:
                if current_hash not in self.known_good_hashes:
                    print(f"Suspicious modification detected: {filepath}")
                    modification_event = {
                        "type": "suspicious_file_modification",
                        "filepath": filepath,
                        "previous_hash": event["hash"],
                        "current_hash": current_hash
                    }
                    self.engine.process_event(modification_event)
        # Update the known hash to the new hash
        previous_hash = self.known_good_hashes.get(filepath)
        self.known_good_hashes[filepath] = current_hash
        if self.engine.is_suspicious(filepath, previous_hash, current_hash):
            print(f"Suspicious modification detected: {filepath}")
            modification_event = {
                "type": "suspicious_file_modification",
                "filepath": filepath,
                "previous_hash": previous_hash,
                "current_hash": current_hash,
            }
            self.responder.respond_to_threat(modification_event)
        else:
            print(f"File has been modified (known good): {filepath}")
            modification_event = {
                "type": "file_modified",
                "filepath": filepath,
                "previous_hash": previous_hash,
                "current_hash": current_hash,
            }
        self.engine.process_event(modification_event)
