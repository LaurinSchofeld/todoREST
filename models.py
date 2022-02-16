"""
    Contains the defintions of our data models/classes
"""
import uuid, json

class List:
    def __init__(self, name: str, entries: list):
        self.name = name
        self.entries = entries
        self.id = str(uuid.uuid4())
        
    @staticmethod
    def can_create_from(todo_list_dict: dict) -> bool:
        """
        returns a boolean value to indicate whether the given dict can be turned into a valid (todo)List object
        """
        if not todo_list_dict.get("name"):
            return False
        elif not todo_list_dict.get("entries"):
            return False
        else:
            for entry in todo_list_dict.get("entries"):
                if not Entry.can_create_from(entry):
                    return False
        return True
            
        
    def to_dict(self) -> dict:
        """
        creates a dictionary from a (todo)List object
        """
        todo_list_dict = dict()
        todo_list_dict["name"] = self.name
        todo_list_dict["entries"] = self.entries
        todo_list_dict["id"] = self.id
        return todo_list_dict
        
        
class User:
    def __init__(self, user_name: str):
        self.user_name = user_name
        self.id = str(uuid.uuid4())
        
        
class Entry:
    def __init__(self, name: str, list_id: str, user_id: str, description = None):
        self.name = name
        self.id = str(uuid.uuid4())
        self.list_id = list_id
        self.user_id = user_id
        self.description = description if description is not None else ""
        
    @staticmethod
    def can_create_from(entry_dict: dict) -> bool:
        """
        returns a boolean value to indicate whether the given dict can be turned into a valid Entry object
        """
        if not entry_dict.get("name"):
            return False
        elif not entry_dict.get("list_id"):
            return False
        elif not entry_dict.get("user_id"):
            return False
        return True