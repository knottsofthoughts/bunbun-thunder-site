import hashlib
import os

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
        if "file_integrity_check" in self.engine.knowledge_base:
            for event in self.engine.knowledge_base["file_integrity_check"]["events"]:
                if event["filepath"] == filepath and event["hash"] != current_hash:
                    print(f"File has been modified: {filepath}")
                    modification_event = {
                        "type": "file_modified",
                        "filepath": filepath,
                        "previous_hash": event["hash"],
                        "current_hash": current_hash
                    }
                    self.engine.process_event(modification_event)
                    break
