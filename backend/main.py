from flask import Flask, request, jsonify, make_response, render_template
from tinydb import TinyDB, Query
import bcrypt
import base64
from userStateManager import UserStateManager


db = TinyDB('../db.json')
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
    print(sessionid)
    return jsonify({"session": sessionid})

def hashText(text):
    hashed_bytes = bcrypt.hashpw(text.encode('utf-8'), bcrypt.gensalt())
    return base64.b64encode(hashed_bytes).decode('utf-8')

def checkHash(hashed_str, normal):
    hashed_bytes = base64.b64decode(hashed_str)
    return bcrypt.checkpw(normal.encode('utf-8'), hashed_bytes)




if __name__ == '__main__':
    app.run(debug=True)

