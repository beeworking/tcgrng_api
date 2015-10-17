from flask import request, jsonify, abort

from user import User
from database import Database
from . import app


@app.route("/register", methods=["POST"])
def register():
    db = Database()

    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return abort(400)

    user = User(username=username, password=password)
    user = db.save(user)

    return jsonify(user.json())


@app.route("/login", methods=["POST"])
def login():
    db = Database()

    username = request.json.get("username")
    password = request.json.get("password")

    user = db.get(User, {"username": username, "password": password})

    if user:
        return jsonify(user.json())
    return abort(400)
