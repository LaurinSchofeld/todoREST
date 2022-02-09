"""
    Contains the defintions of our data models/classes
"""
import uuid, json

class List:
    def __init__(self, name, entries):
        self.name = name
        self.entries = entries
        self.id = str(uuid.uuid4())
        
    def list_completed(self):
        for entry in self.entries:
            if not entry.completed:
                return False
        return True
        
        
class User:
    def __init__(self, user_name):
        self.user_name = user_name
        self.id = str(uuid.uuid4())
        
        
class Entry:
    def __init__(self, name, list_id, user_id, description = None):
        self.name = name
        self.id = str(uuid.uuid4())
        self.list_id = list_id
        self.user_id = user_id
        self.description = description if description is not None else ""