import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Endpoint untuk menerima dan menyimpan pesan penggemar
@app.route("/fan_message", methods=["POST"])
def fan_message_post():
    nickname_receive = request.form['nickname_give']
    message_receive = request.form['message_give']

    doc = {
        'nickname': nickname_receive,
        'message': message_receive
    }

    db.fan_messages.insert_one(doc)
    return jsonify({'msg': 'Fan message saved successfully!'})

# Endpoint untuk menampilkan pesan penggemar
@app.route("/fan_messages", methods=["GET"])
def fan_messages_get():
    messages_list = list(db.fan_messages.find({}, {'_id': False}))
    return jsonify({'messages': messages_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
