import json, uuid
from models import List, Entry, User
from flask import abort

class Controller:
    def __init__(self, lists=None, users=None):
        self.lists = lists or dict()
        self.users = users or dict()
        
        
    @staticmethod
    def validate_uuid(id_to_validate, err_code=None):
        """
        Versucht aus dem uuid string eine uuid zu erstellen und gibt entweder den id string zurück oder bricht den request mit Fehlercode ab.
        """
        try:
            valid_id = uuid.UUID(id_to_validate, version=4)
            valid_id = str(valid_id)
            return valid_id
        except ValueError as ve:
            err_code = err_code or 404
            abort(err_code, "Die angegebene id ist ungültig. Es muss eine uuid übergeben werden.\n" + str(ve))
    
    
    def get_request_data(self, request):
        """
        Decodiert die Daten aus dem request body und gibt sie als dictionary zurück.
        """
        try:
            request_data = request.data
            request_data = request_data.decode(request.charset)
            return json.loads(request_data)
        except Exception as e:
            print(str(e))
            abort(500, "Die Daten konnten nicht aus dem request geparsed werden.")
            
            
    def add_list(self, request):
        """
        Fügt eine neue Liste hinzu.
        """
        list_dict = self.get_request_data(request)
        if list_dict is not None and List.can_create_from(list_dict):
            new_todo_list = List(list_dict.get("name"), list_dict.get("entries"))
            self.lists[new_todo_list.id] = new_todo_list
            return json.dumps(new_todo_list.to_dict())
        abort(500, "Es konnte keine neue Liste mit den angegebenen Daten angelegt werden.")
        
        
    def get_list_entries(self, list_id):
        """
        Gibt eine Liste aller Einträge einer Todo-Liste zurück.
        """
        td_list = self.lists.get(list_id)
        if td_list:
            return json.dumps(list(td_list.entries.values()))
        abort(404, f"Die Liste mit der id: {list_id} konnte nicht gefunden werden.")
        
        
    def delete_list(self, list_id):
        """
        Löscht eine Liste.
        """
        td_list = self.lists.get(list_id)
        if td_list:
            del self.lists[list_id]
            return "Liste erfolgreich gelöscht."
        abort(404, f"Die Liste mit der id: {list_id} konnte nicht gefunden werden.")
        
        
    def add_entry(self, list_id, request):
        """
        Fügt einer Liste einen neuen Eintrag hinzu.
        """
        entry_dict = self.get_request_data(request)
        if entry_dict:
            entry_dict["list_id"] = list_id
            if Entry.can_create_from(entry_dict):
                new_entry = Entry.create_from_dict(entry_dict)
                td_list = self.lists.get(list_id)
                if td_list:
                    td_list.entries[new_entry.id] = new_entry
                    return json.dumps(new_entry.to_dict())
                else:
                    abort(500, f"Die Liste mit der id: {list_id} konnte nicht gefunden werden.")
        abort(500, "Es konnte kein neuer Eintrag mit den angegebenen Daten angelegt werden.")
            
            
    def update_entry(self, list_id, entry_id, request):
        """
        Ändert einen Eintrag.
        """
        update_data = self.get_request_data(request)
        td_list = self.lists.get(list_id)
        if td_list:
            entry = td_list.entries.get(entry_id)
            if entry:
                for key, new_value in update_data.items():
                    if key == "name":
                        entry.name = new_value
                    elif key == "description":
                        entry.description = new_value
                    elif key == "list_id":
                        new_list_id = Controller.validate_uuid(new_value)
                        if new_list_id != entry.list_id:
                            entry.list_id = new_list_id
                    elif key == "user_id":
                        new_user_id = Controller.validate_uuid(new_value)
                        if new_user_id != entry.user_id:
                            entry.user_id = new_user_id
                return "Eintrag erfolgreich aktualisiert."
            else:
                abort(404, f"Der Eintrag mit der id: {entry_id} konnte nicht gefunden werden.")
        else:
            abort(404, f"Die Liste mit der id: {list_id} konnte nicht gefunden werden.")
            
            
    def delete_entry(self, list_id, entry_id):
        """
        Löscht einen Eintrag.
        """
        td_list = self.lists.get(list_id)
        if td_list:
            entry = td_list.get(entry_id)
            if entry:
                del td_list[entry_id]
                return "Eintrag erfolgreich gelöscht."
            else:
                abort(404, f"Der Eintrag mit der id: {entry_id} konnte nicht gefunden werden.")
        else:
            abort(404, f"Die Liste mit der id: {list_id} konnte nicht gefunden werden.")
            
            
    def get_all_users(self):
        """
        Gibt eine Liste aller Nutzer zurück.
        """
        user_list = list()
        for user in self.users.values():
            user_list.append({"username": user.username, "id": user.id})
        return json.dumps(user_list)
        
    def add_user(self, request):
        """
        Fügt einen neuen Nutzer hinzu und gibt die Daten von diesem als json string zurück.
        """
        new_user_data = self.get_request_data(request)
        username = new_user_data.get("username")
        if username:
            new_user = User(username)
            self.users[new_user.id] = new_user
            new_user_dict = {"username": new_user.username, "id": new_user.id}
            return json.dumps(new_user_dict)
        else:
            abort(500, "Es konnte kein neuer User mit den angegebenen Daten angelegt werden.")
        
        
    def delete_user(self, user_id):
        """
        Löscht einen Nutzer.
        """
        user = self.users.get(user_id)
        if user:
            del self.users[user_id]
            return  f"User {user.username} erfolgreich gelöscht."
        else:
            abort(404, f"Der User mit der id: {user_id} konnte nicht gefunden werden.")
                    