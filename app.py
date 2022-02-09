from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Dies ist die Todo-Listen API</h1>"


if __name__ == "__main__":
    app.run(port=8000)
    