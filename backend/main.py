from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import bcrypt
import base64
from userStateManager import UserStateManager


db = TinyDB('../db.json')
usm = UserStateManager()
app = Flask(__name__)



@app.route('/register', methods = ["POST"])
def register():
    data = request.json

    if data["username"] == "" or data["password"] == "":
        return jsonify({"status": "fail", "error": "invalid data"})

    User = Query()
    if db.search(User.username == data["username"]):
        return jsonify({"status": "fail", "error": "user already exists"})
    
    db.insert({"username": data["username"], "password": hashText(data["password"])})


    return jsonify({"status": "success"})

@app.route('/login', methods = ["POST"])
def login():
    data = request.json

    User = Query()
    users = db.search(User.username == data["username"])
    
    user = None
    if len(users) > 0:
        user = users[0]
    

    if not user or not checkHash(user["password"], data["password"]):
        return jsonify({"status": "fail", "error": "invalid credentials"})
    


    
    print(user)

    return jsonify({"status": "success"})


def hashText(text):
    hashed_bytes = bcrypt.hashpw(text.encode('utf-8'), bcrypt.gensalt())
    return base64.b64encode(hashed_bytes).decode('utf-8')

def checkHash(hashed_str, normal):
    hashed_bytes = base64.b64decode(hashed_str)
    return bcrypt.checkpw(normal.encode('utf-8'), hashed_bytes)




if __name__ == '__main__':
    app.run(debug=True)

