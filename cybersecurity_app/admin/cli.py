import argparse
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.engine import CoreEngine

def main():
    parser = argparse.ArgumentParser(description="Cybersecurity App Admin CLI")
    subparsers = parser.add_subparsers(dest="command")

    # View events
    view_parser = subparsers.add_parser("view", help="View events by type")
    view_parser.add_argument("--type", required=True, help="Type of the event to view")

    # Add event
    add_parser = subparsers.add_parser("add", help="Add a new event")
    add_parser.add_argument("--type", required=True, help="Type of the event")
    add_parser.add_argument("--user", help="User associated with the event")
    add_parser.add_argument("--success", action="store_true", help="Whether the event was successful")

    args = parser.parse_args()
    engine = CoreEngine()

    if args.command == "view":
        events = engine.get_events_by_type(args.type)
        print(json.dumps(events, indent=4))
    elif args.command == "add":
        event = {"type": args.type}
        if args.user:
            event["user"] = args.user
        if args.success:
            event["success"] = args.success
        engine.process_event(event)
        print("Event added successfully.")

if __name__ == "__main__":
    main()
