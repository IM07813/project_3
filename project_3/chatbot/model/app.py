from flask import Flask, render_template, request, jsonify
from chatbot import response
import chatbot
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_query = request.form["query"]
    response = response(user_query)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)