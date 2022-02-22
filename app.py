from flask import Flask, request
from controller import Controller

app = Flask(__name__)
controller = Controller()

@app.route("/")
def hello_world():
    return "<h1 style='text-align:center; font-size: 4em'>Dies ist die <a href='https://github.com/LaurinSchofeld/todoREST' target='_blank'>Todo-Listen API</a></h1>"

@app.route("/list/<list_id>/", methods=["GET", "DELETE"])
def get_delete_list(list_id):
    validated_id = Controller.validate_uuid(list_id)
    if request.method == "GET":
        return controller.get_list_entries(validated_id)
    elif request.method == "DELETE":
        return controller.delete_list(validated_id)

@app.route("/list/", methods=["POST"])
def add_list():
    return controller.add_list(request)
    
@app.route("/list/<list_id>/entry/", methods=["POST"])   
def add_entry(list_id):
    validated_id = Controller.validate_uuid(list_id)
    return controller.add_entry(validated_id, request)


#@app.route("", methods=[""])   
#@app.route("", methods=[""])   
#@app.route("", methods=[""])    
    
if __name__ == "__main__":
    app.debug = True
    app.run(port=8000)
    