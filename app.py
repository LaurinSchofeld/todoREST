from flask import Flask, request, abort
from models import List, Entry, User
import json, controller

app = Flask(__name__)

lists = []

@app.route("/")
def hello_world():
    return "<h1>Dies ist die Todo-Listen API</h1>"

@app.route('/list/', methods=['POST'])
def add_list():
    request_data = request.get_json()
    if request_data is None or not List.can_create_from(request_data):
        return abort(500, "It seems the data in your request did not satisfy the requrements to create a new Todo List.")
    else:
        new_todo_list = List(request_data.get("name"), request_data.get("entries"))
        lists.append(new_todo_list)
        return json.dumps(new_todo_list.to_dict())
    
    return abort(500)
    


if __name__ == "__main__":
    app.run(port=8000)
    