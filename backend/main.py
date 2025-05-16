from flask import Flask, request, jsonify, make_response, render_template
from tinydb import TinyDB, Query
import bcrypt
import base64
from datetime import datetime
from userStateManager import UserStateManager


db = TinyDB('../db.json')

user_table = db.table("users")
actions_table = db.table("actions")
action_log_table = db.table("action_logs")
mood_log_table = db.table("mood_logs")

query = Query()

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

    
    if user_table.search(query.username == data["username"]):
        return jsonify({"status": "fail", "error": "user already exists"})
    
    user_table.insert({"username": data["username"], "password": hashText(data["password"])})


    return jsonify({"status": "success"})

@app.route('/login', methods = ["POST"])
def login():
    data = request.json

    
    users = user_table.search(query.username == data["username"])
    
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
    
    user = user_table.search(query.username == usm.get_user(sessionid))
    if(not user):
        return jsonify({"status": "fail"}), 401
    else:
        user = user[0]



    data = request.json

    vse = actions_table.all()

    novId = newId(vse)
    
    actions_table.insert({"id": novId, "name": data["name"], "impact": data["impact"], "username": user["username"]})

    return jsonify({"status": "success"})

@app.route("/get_actions", methods=["POST"])
def get_actions():
    sessionid = request.cookies.get("sessionid")
    
    user = user_table.search(query.username == usm.get_user(sessionid))
    if(not user):
        return jsonify({"status": "fail"}), 401
    else:
        user = user[0]


    vse = actions_table.search(query.username == user["username"])
    return jsonify({"status": "success", "actions": vse})
    
@app.route("/delete_action", methods=["POST"])
def delete_action():
    sessionid = request.cookies.get("sessionid")
    
    user = user_table.search(query.username == usm.get_user(sessionid))
    if(not user):
        return jsonify({"status": "fail"}), 401
    else:
        user = user[0]

    data = request.json
    actions = actions_table.search(query.id == data.get("id"))

    if not actions:
        return jsonify({"status": "fail"})

    actions_table.remove(query.id == actions[0]["id"])

    return jsonify({"status": "success"})
    

@app.route("/edit_action", methods=["POST"])
def edit_action():
    sessionid = request.cookies.get("sessionid")
    
    user = validateUser(sessionid)
    if not user:
        return jsonify({"status": "fail"}), 401

    data = request.json
    actions = actions_table.search(query.id == data.get("id"))

    if not actions:
        return jsonify({"status": "fail"})
    
    actions_table.update(
        {'impact': data['impact'], 'name': data['name']},
        query.id == data['id']
    )

    return jsonify({"status": "success"})

@app.route("/save_mood", methods=["POST"])
def save_mood():
    sessionid = request.cookies.get("sessionid")
    
    user = validateUser(sessionid)
    if not user:
        return jsonify({"status": "fail"}), 401

    data = request.json

    novId = newId(mood_log_table.all())

    zdajStr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    mood_log_table.insert({"id": novId, "mood": data["level"], "time": zdajStr, "username": user["username"]})


    return jsonify({"status": "success"})


@app.route("/save_action", methods=["POST"])
def save_action():
    sessionid = request.cookies.get("sessionid")

    user = validateUser(sessionid)
    if not user:
        return jsonify({"status": "fail"}), 401
    
    data = request.json # rabmo action id pa duration

    novId = newId(action_log_table.all())

    zdajStr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    action_log_table.insert({"id": novId, "action_id": data["action_id"], "duration_minutes": data["duration_minutes"], "time": zdajStr, "username": user["username"]})

    return jsonify({"status": "success"})



def newId(sez: list[object]):
    minId = 0
    for e in sez:
        if e["id"] > minId: minId = e["id"]
    return minId + 1


def validateUser(sessionid):
    user = user_table.search(query.username == usm.get_user(sessionid))
    if not user:
        return False
    
    return user[0]

if __name__ == '__main__':
    app.run(debug=True)


