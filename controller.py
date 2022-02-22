import json, uuid
from models import List, Entry, User
from flask import abort

class Controller:
    def __init__(self, lists=[]):
        self.lists = lists
        
    @staticmethod
    def validate_uuid(id_to_validate):
        try:
            valid_id = uuid.UUID(id_to_validate, version=4)
            valid_id = str(valid_id)
            return valid_id
        except ValueError as ve:
            abort(404, "Die angegebene id ist ungültig. Es muss eine uuid übergeben werden.\n" + str(ve))
        
    def add_list(self, request):
        request_data = request.get_json()
        if request_data is not None and List.can_create_from(request_data):
            new_todo_list = List(request_data.get("name"), request_data.get("entries"))
            self.lists.append(new_todo_list)
            return json.dumps(new_todo_list.to_dict())
        else:
            abort(500, "Es konnte keine neue Liste aus den angegebenen Daten erstellt werden.")
        
    def get_list_entries(self, list_id):
        for td_list in self.lists:
            if td_list.id == list_id:
                return json.dumps(td_list.get("entries"))
        abort(404, f"Die Liste mit der id: {list_id} konnte nicht gefunden werden.")
        
    def delete_list(self, list_id):
        for td_list in self.lists:
            if td_list.id == list_id:
                self.lists.remove(td_list)
                return "Eintrag erfolgreich gelöscht."
        abort(404, f"Die Liste mit der id: {list_id} konnte nicht gefunden werden.")
        
    def add_entry(self, list_id, request):
        entry_dict = request.get_json()
        if entry_dict and Entry.can_create_from(entry_dict):
            new_entry = Entry.create_from_dict(entry_dict)
            for list in self.lists:
                if list.id == list_id:
                    list.entries.append(new_entry)