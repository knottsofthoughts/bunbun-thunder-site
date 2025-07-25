import json

class CoreEngine:
    def __init__(self, knowledge_base_path="knowledge_base.json"):
        self.knowledge_base_path = knowledge_base_path
        self.load_knowledge_base()

    def process_event(self, event):
        # Placeholder for event processing logic
        print(f"Processing event: {event}")
        self.learn_from_event(event)

    def learn_from_event(self, event):
        # More sophisticated learning logic will be added here
        print(f"Learning from event: {event}")
        event_type = event.get("type")
        if event_type:
            if event_type not in self.knowledge_base:
                self.knowledge_base[event_type] = {"count": 0, "events": []}
            self.knowledge_base[event_type]["count"] += 1
            self.knowledge_base[event_type]["events"].append(event)
        self.save_knowledge_base()

    def load_knowledge_base(self):
        try:
            with open(self.knowledge_base_path, "r") as f:
                self.knowledge_base = json.load(f)
        except FileNotFoundError:
            self.knowledge_base = {}

    def save_knowledge_base(self):
        with open(self.knowledge_base_path, "w") as f:
            json.dump(self.knowledge_base, f, indent=4)
