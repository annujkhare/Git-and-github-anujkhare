from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

db = client["flask_assignment"]
collection = db["submissions"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        return jsonify(data)

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


@app.route("/submit", methods=["POST"])
def submit():

    try:
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email or not message:
            return render_template(
                "index.html",
                error="All fields are required."
            )

        data = {
            "name": name,
            "email": email,
            "message": message
        }

        collection.insert_one(data)

        return redirect(url_for("success"))

    except Exception as error:
        return render_template(
            "index.html",
            error=str(error)
        )

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    try:
        
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        item_name = data.get("itemName")
        item_description = data.get("itemDescription")

        
        if not item_name or not item_description:
            return jsonify({
                "error": "Item name and description are required"
            }), 400

        
        todo_item = {
            "itemName": item_name,
            "itemDescription": item_description
        }

        db["todo_items"].insert_one(todo_item)

        return jsonify({
            "message": "To-Do item saved successfully"
        }), 201

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500

@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)