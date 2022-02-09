from flask import Flask, request, Response
from models import List, Entry, User
import json, controller

app = Flask(__name__)

lists = []

@app.route("/")
def hello_world():
    return "<h1>Dies ist die Todo-Listen API</h1>"

@app.route('/list', methods=['POST'])
def add_list():
    request_data = request.get_json(force=True)
    list_name = request_data["name"]
    list_entries = request_data["entries"]
    new_list = List(list_name, list_entries)
    lists.append(new_list)
    ret = {"name": new_list.name, "entries": new_list.entries, "id": new_list.id}
    return json.dumps(ret)


if __name__ == "__main__":
    app.run(port=8000)
    