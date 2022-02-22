from flask import Flask, request
from controller import Controller

app = Flask(__name__)
controller = Controller()

@app.route("/")
def hello_world():
    return "<h1 style='text-align:center; font-size: 4em'>Dies ist die <a href='https://github.com/LaurinSchofeld/todoREST' target='_blank'>Todo-Listen API</a></h1>"


@app.route("/list/<list_id>", methods=["GET", "DELETE"])
def get_delete_list(list_id):
    valid_id = Controller.validate_uuid(list_id)
    if request.method == "GET":
        return controller.get_list_entries(valid_id)
    elif request.method == "DELETE":
        return controller.delete_list(valid_id)


@app.route("/list/", methods=["POST"])
def add_list():
    return controller.add_list(request)
    
    
@app.route("/list/<list_id>/entry/", methods=["POST"])   
def add_entry(list_id):
    valid_id = Controller.validate_uuid(list_id, 500)
    return controller.add_entry(valid_id, request)


@app.route("/list/<list_id>/entry/<entry_id>", methods=["POST", "DELETE"])   
def update_delete_entry(list_id, entry_id):
    valid_list_id = Controller.validate_uuid(list_id)
    valid_entry_id = Controller.validate_uuid(entry_id)
    if request.method == "POST":
        return controller.update_entry(valid_list_id, valid_entry_id, request)
    elif request.method == "DELETE":
        return controller.delete_entry(valid_list_id, valid_entry_id)


@app.route("/users/", methods=["GET"])
def get_all_users():
    return controller.get_all_users()
   
        
@app.route("/user/", methods=["POST"])    
def add_user():
    return controller.add_user(request)


@app.route("/user/<user_id>", methods=["DELETE"])    
def delete_user(user_id):
    valid_user_id = Controller.validate_uuid(user_id)
    return controller.delete_user(valid_user_id) 
    
    
if __name__ == "__main__":
    app.run(port=8000)
    