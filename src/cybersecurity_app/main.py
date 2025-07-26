from cybersecurity_app.core.engine import CoreEngine
from cybersecurity_app.features.file_integrity import FileIntegrityMonitor

if __name__ == "__main__":
    engine = CoreEngine()
    file_monitor = FileIntegrityMonitor(engine)
    # Create a test file to be monitored
    with open("test_file.txt", "w") as f:
        f.write("This is a test file.")
    file_monitor.monitor_file("test_file.txt")
    # Modify the test file to trigger a suspicious modification
    with open("test_file.txt", "w") as f:
        f.write("This is a malicious modification.")
    file_monitor.monitor_file("test_file.txt")
    print("Cybersecurity App Initialized")
