import uuid

class Entry:
    def __init__(self, name, completed):
        self.name = name
        self.id = str(uuid.uuid4())
        self.completed = completed