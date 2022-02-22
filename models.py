import uuid

class List:
    def __init__(self, name: str, entries=None):
        self.name = name
        self.entries = entries or dict()
        self.id = str(uuid.uuid4())
        
    @staticmethod
    def can_create_from(todo_list_dict: dict) -> bool:
        """
        Gibt einen bool Wert zurück, der aussagt, ob man aus dem angegebenen Dictionary ein Objekt vom Typ List erstellen kann
        """
        if not todo_list_dict.get("name"):
            return False
        elif todo_list_dict.get("entries") is not None:
            for entry in todo_list_dict.get("entries"):
                if not Entry.can_create_from(entry):
                    return False
        return True  
        
    def to_dict(self) -> dict:
        """
        Gibt ein Dictionary zurück, welches die aktuelle Instanz des List Objektes darstellt
        """
        todo_list_dict = dict()
        todo_list_dict["name"] = self.name
        todo_list_dict["entries"] = self.entries
        todo_list_dict["id"] = self.id
        return todo_list_dict
    
        
class User:
    def __init__(self, username: str):
        self.username = username
        self.id = str(uuid.uuid4())
        
       
class Entry:
    def __init__(self, name: str, list_id: str, user_id: str, description=None):
        self.name = name
        self.id = str(uuid.uuid4())
        self.list_id = list_id
        self.user_id = user_id
        self.description = description or ""
        
    @staticmethod
    def can_create_from(entry_dict: dict) -> bool:
        """
        Gibt einen bool Wert zurück, der aussagt, ob man aus dem angegebenen Dictionary ein Objekt vom Typ Entry erstellen kann
        """
        if not entry_dict.get("name"):
            return False
        elif not entry_dict.get("list_id"):
            return False
        elif not entry_dict.get("user_id"):
            return False
        return True
    
    @staticmethod
    def create_from_dict(entry_dict: dict):
        """
        Erstellt einen neuen Listeneintrag anhand eines Dictionarys
        """
        name = entry_dict.get("name")
        list_id = entry_dict.get("list_id")
        user_id = entry_dict.get("user_id")
        description = entry_dict.get("description")
        return Entry(name, list_id, user_id, description)
    