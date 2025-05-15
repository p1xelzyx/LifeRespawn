from flask import Flask, request, jsonify, make_response, render_template
from tinydb import TinyDB, Query
import bcrypt
import base64
from userStateManager import UserStateManager


db = TinyDB('../db.json')
user_table = db.table("users")
actions_table = db.table("actions")

User = Query()

usm = UserStateManager()
app = Flask(__name__)

@app.route("/")
def test():
    print("test")
    return render_template("index.html")

@app.route('/register', methods = ["POST"])
def register():
    data = request.json

    if data["username"] == "" or data["password"] == "":
        return jsonify({"status": "fail", "error": "invalid data"})

    
    if user_table.search(User.username == data["username"]):
        return jsonify({"status": "fail", "error": "user already exists"})
    
    user_table.insert({"username": data["username"], "password": hashText(data["password"])})


    return jsonify({"status": "success"})

@app.route('/login', methods = ["POST"])
def login():
    data = request.json

    
    users = user_table.search(User.username == data["username"])
    
    user = None
    if len(users) > 0:
        user = users[0]
    

    if not user or not checkHash(user["password"], data["password"]):
        return jsonify({"status": "fail", "error": "invalid credentials"})
    
    

    usm.login_user(user["username"])
    
    resp = make_response(jsonify({"status": "success"}))
    resp.set_cookie(
        'sessionid', 
        usm.users[user["username"]],
        httponly=True,  # Prevents JavaScript access
        secure=True,    # Ensure cookie is sent over HTTPS only
        samesite="Lax", # Helps protect against CSRF
    )


    return resp

@app.route("/logout", methods=["POST"])
def logout():
    sessionid = request.cookies.get("sessionid")
    print(sessionid)
    try:
        usm.logout_user(usm.get_user(sessionid))
        resp = make_response(jsonify({"status": "success"}))
        resp.delete_cookie("sessionid")
        return resp
    except:
        return jsonify({"status": "fail"})


@app.route("/check_session", methods=["POST"])
def check_session():
    sessionid = request.cookies.get("sessionid")
    return jsonify({"username": usm.get_user(sessionid)})

def hashText(text):
    hashed_bytes = bcrypt.hashpw(text.encode('utf-8'), bcrypt.gensalt())
    return base64.b64encode(hashed_bytes).decode('utf-8')

def checkHash(hashed_str, normal):
    hashed_bytes = base64.b64decode(hashed_str)
    return bcrypt.checkpw(normal.encode('utf-8'), hashed_bytes)

@app.route("/new_action", methods=["POST"])
def new_action():
    sessionid = request.cookies.get("sessionid")
    
    user = user_table.search(User.username == usm.get_user(sessionid))[0]

    if not user:
        return jsonify({"status": "fail"})

    data = request.json

    vse = actions_table.all()

    maxId = 0
    for a in vse:
        if a["id"] > maxId:
            maxId = a["id"]
    
    actions_table.insert({"id": maxId + 1, "name": data["name"], "impact": data["impact"], "username": user["username"]})

    return jsonify({"status": "success"})

@app.route("/get_actions", methods=["POST"])
def get_actions():
    sessionid = request.cookies.get("sessionid")
    
    user = user_table.search(User.username == usm.get_user(sessionid))[0]

    if not user:
        return jsonify({"status": "fail"})

    vse = actions_table.search(User.username == user["username"])
    return jsonify({"status": "success", "actions": vse})
    


if __name__ == '__main__':
    app.run(debug=True)

