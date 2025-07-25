import os
import shutil

class ThreatResponder:
    def __init__(self, engine):
        self.engine = engine
        self.quarantine_dir = "quarantine"

    def respond_to_threat(self, event):
        """Responds to a threat event."""
        if event["type"] == "suspicious_file_modification":
            self.quarantine_file(event["filepath"])

    def quarantine_file(self, filepath):
        """Moves a file to the quarantine directory."""
        if os.path.exists(filepath):
            quarantine_path = os.path.join(self.quarantine_dir, os.path.basename(filepath))
            print(f"Quarantining file: {filepath} -> {quarantine_path}")
            shutil.move(filepath, quarantine_path)
            event = {
                "type": "file_quarantined",
                "filepath": filepath,
                "quarantine_path": quarantine_path
            }
            self.engine.process_event(event)
