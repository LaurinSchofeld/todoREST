import uuid

class List:
    def __init__(self, name: str, entries=None):
        self.name = name
        self.entries = dict()
        self.id = str(uuid.uuid4())
        if entries:
            # entries wird als array eingegeben, ist intern aber ein dictionary
            for entry in entries:
                # Beim anlegen einer Liste bekommt jeder Eintrag die ID der Liste.
                if "list_id" in entry.keys():
                    del entry["list_id"]
                entry["list_id"] = self.id
                if Entry.can_create_from(entry):
                    entry = Entry.create_from_dict(entry)
                    self.entries[entry.id] = entry
                
                
    @staticmethod
    def can_create_from(todo_list_dict: dict) -> bool:
        """
        Gibt einen bool Wert zurück, der aussagt, ob man aus dem angegebenen Dictionary ein Objekt vom Typ List erstellen kann
        """
        if not todo_list_dict.get("name"):
            return False
        elif todo_list_dict.get("entries") is not None:
            for entry in todo_list_dict.get("entries"):
                if not Entry.can_create_from(entry, ignore_field="list_id"):
                    return False
        return True  
        
    def to_dict(self) -> dict:
        """
        Gibt ein Dictionary zurück, welches die aktuelle Instanz des List Objektes darstellt
        """
        todo_list_dict = dict()
        todo_list_dict["name"] = self.name
        # entries ist ein dictionary, wollen es als list zurückgeben
        todo_list_dict["entries"] = [entry.to_dict() for entry in self.entries.values()] 
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
    def can_create_from(entry_dict: dict, ignore_field="") -> bool:
        """
        Gibt einen bool Wert zurück, der aussagt, ob man aus dem angegebenen Dictionary ein Objekt vom Typ Entry erstellen kann
        """
        field_names = ["name", "list_id", "user_id"]
        for field_name in field_names:
            # ignore_field wird verwendet, damit man auch beim anlegen einer neuen liste einträge hinterlegen kann, obwohl diese noch keine list_id haben
            # dict.get(schlüssel) gibt den wert mit dem gesuchten schlüssel oder None zurück
            if not entry_dict.get(field_name) and not ignore_field == field_name:
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
    
    def to_dict(self) -> dict:
        """
        Gibt ein Dictionary zurück, welches die aktuelle Instanz des List Objektes darstellt
        """
        entry_dict = dict()
        entry_dict["name"] = self.name
        entry_dict["id"] = self.id
        entry_dict["list_id"] = self.list_id
        entry_dict["user_id"] = self.user_id
        entry_dict["description"] = self.description

        return entry_dict