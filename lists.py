import uuid, json

class List:
    def __init__(self, name, entries):
        self.name = name
        self.entries = entries or []
        self.id = str(uuid.uuid4())
        self.completed = self.list_completed() if entries else False
        
    def list_completed(self):
        for entry in self.entries:
            if not entry.completed:
                return False
        return True
        