from core.engine import CoreEngine
from features.file_integrity import FileIntegrityMonitor

if __name__ == "__main__":
    engine = CoreEngine()
    file_monitor = FileIntegrityMonitor(engine)

    # Monitor the knowledge_base.json file
    file_monitor.monitor_file("knowledge_base.json")

    print("Cybersecurity App Initialized")
