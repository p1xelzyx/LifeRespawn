from flask import Flask, request, jsonify, make_response, render_template
from tinydb import TinyDB, Query
import bcrypt
import base64
from datetime import datetime, date as dateObj
from userStateManager import UserStateManager
import calendar


db = TinyDB('../db.json')

user_table = db.table("users")
actions_table = db.table("actions")
action_log_table = db.table("action_logs")
mood_log_table = db.table("mood_logs")
goal_table = db.table("goals")
mission_table = db.table("missions")

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

    #actions_table.remove(query.id == actions[0]["id"])
    actions_table.update({"username": ""}, query.id == actions[0]["id"])

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

    dur = data.get("duration_minutes", False)

    action_log_table.insert({"id": novId, "action_id": data["action_id"], "duration_minutes": dur, "amount": 1 if dur is False else 0 ,"time": zdajStr, "username": user["username"]})


    return jsonify({"status": "success"})

@app.route("/new_goal", methods=["POST"])
def new_goal():
    sessionid = request.cookies.get("sessionid")

    user = validateUser(sessionid)
    if not user:
        return jsonify({"status": "fail"}), 401
    
    data = request.json

    novId = newId(goal_table.all())

    zdajStr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    goal_table.insert({"id": novId, "action_id": data["action_id"], "duration_minutes": data.get("duration_minutes", False), "amount": data.get("amount", False), "username": user["username"], "positive": data["positive"], "days": data["days"], "date_created": zdajStr, "date_deleted": False})

    return jsonify({"status": "success"})


@app.route("/get_goals", methods=["POST"])
def get_goals():
    sessionid = request.cookies.get("sessionid")
    
    user = user_table.search(query.username == usm.get_user(sessionid))
    if(not user):
        return jsonify({"status": "fail"}), 401
    else:
        user = user[0]


    vse = [g for g in goal_table.search(query.username == user["username"]) if g["date_deleted"] is False]
    
    print(vse)
    return jsonify({"status": "success", "goals": vse})


@app.route("/delete_goal", methods=["POST"])
def delete_goal():
    sessionid = request.cookies.get("sessionid")
    
    user = user_table.search(query.username == usm.get_user(sessionid))
    if(not user):
        return jsonify({"status": "fail"}), 401
    else:
        user = user[0]

    data = request.json
    goals = goal_table.search(query.id == data.get("goal_id"))

    if not goals:
        return jsonify({"status": "fail"})

    zdajStr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    goal_table.update({"date_deleted": zdajStr}, query.id == goals[0]["id"])

    return jsonify({"status": "success"})

@app.route("/update_goal_day", methods=["POST"])
def update_goal_day():
    sessionid = request.cookies.get("sessionid")
    
    user = user_table.search(query.username == usm.get_user(sessionid))
    if(not user):
        return jsonify({"status": "fail"}), 401
    else:
        user = user[0]

    data = request.json
    goals = goal_table.search(query.id == data.get("goal_id"))

    if not goals:
        return jsonify({"status": "fail"})
    
    current = goals[0]["days"]

    current[data["day"]] = 0 if current[data["day"]] else 1 


    goal_table.update({"days": current}, query.id == goals[0]["id"])

    return jsonify({"status": "success"})


@app.route("/check_goals_today", methods=["POST"])
def check_goals_today():
    sessionid = request.cookies.get("sessionid")
    
    user = user_table.search(query.username == usm.get_user(sessionid))
    if(not user):
        return jsonify({"status": "fail"}), 401
    else:
        user = user[0]

    # rabmo vse gole userja, jih filtrirat po keri so dons veljavni
    # rabmo vse actione userja
    # rabmo action log userja za dons



    goals = goal_table.search(query.username == user["username"])
    weekDay = datetime.today().weekday()
    dateToday = datetime.today().date()
    actions = actions_table.search(query.username == user["username"])
    
    
    logs = [l for l in action_log_table.search(query.username == user["username"]) if datetime.strptime(l["time"], "%Y-%m-%d %H:%M:%S").date() == dateToday]
    
    final = []
    for goal in goals: 
        if not goal["days"][weekDay]: continue

        action = next((a for a in actions if a["id"] == goal["action_id"]), None)

        goalUnit = "amount" if goal["amount"] else "duration_minutes"

        full = 0
        for log in logs:
            if log["action_id"] != action["id"]: continue
            print(log)
            full += log[goalUnit] # VELIK PROBLEM: dela za enkrat ampak treba popravt frontend in sistem actionov. verjetna rešitev: treba bo spremenit action v frontend ko nardiš da je amount alpa duration, tkoda se pol to nebo mešal. ker zdej lahko action log nardiš kot čs alpa amount in to nima smila ker je goal lahko samo eno ali drugo. npr user lahko ponesreči beleži action kor amount ampak ma goal nastavljen na duration in pol se bo štelo +1 minuta kokr je user mislu +1 amount ko je beležil to mu mormo dat stran opcijo da to nardi
        
        goalFull = goal[goalUnit]

        final.append({"name": action["name"], "current": full, "goal": goalFull, "unit": goalUnit, "positive": goal["positive"]})

    return jsonify({"status": "success", "analysis": final})



@app.route("/save_mission", methods=["POST"])
def save_mission():
    sessionid = request.cookies.get("sessionid")

    user = validateUser(sessionid)
    if not user:
        return jsonify({"status": "fail"}), 401
    
    data = request.json # ime, desc opt., priorty 0-2 

    novId = newId(mission_table.all())

    mission_table.insert({"id": novId, "name": data["name"], "description": data.get("description", ""), "priority": data["priority"], "username": user["username"], "completed": 0})


    return jsonify({"status": "success"})

@app.route("/get_missions", methods=["POST"])
def get_missions():
    sessionid = request.cookies.get("sessionid")

    user = validateUser(sessionid)
    if not user:
        return jsonify({"status": "fail"}), 401
    
    allFresh = mission_table.search((query.username == user["username"]) & (query.completed == 0))
    
    print(allFresh)

    return jsonify({"status": "success", "missions": allFresh})
    
@app.route("/delete_mission", methods=["POST"])
def delete_mission():
    sessionid = request.cookies.get("sessionid")

    user = validateUser(sessionid)
    if not user:
        return jsonify({"status": "fail"}), 401
    
    data = request.json
    missions = actions_table.search(query.id == data.get("id"))

    if not missions:
        return jsonify({"status": "fail"})

    mission_table.update({"completed": -1}, query.id == data["id"])

    return jsonify({"status": "success"})

@app.route("/complete_mission", methods=["POST"])
def complete_mission():
    sessionid = request.cookies.get("sessionid")

    user = validateUser(sessionid)
    if not user:
        return jsonify({"status": "fail"}), 401
    
    data = request.json
    missions = actions_table.search(query.id == data.get("id"))

    if not missions:
        return jsonify({"status": "fail"})

    mission_table.update({"completed": 1}, query.id == data["id"])

    return jsonify({"status": "success"})

@app.route("/goal_history", methods=["POST"])
def goal_history():
    sessionid = request.cookies.get("sessionid")

    user = validateUser(sessionid)
    if not user:
        return jsonify({"status": "fail"}), 401
    
    data = request.json
    # gremo skos vse dneve. za vsak dan pogledamo keri goli so bli tm (if date created >= dan, dan weekday je v goalovih weekdayih )
    # mamo dan z goli, za vsak gol je treba prevert actione za točn tist dan in nardit za vsak gol za vrnt: ime, kok, goal kok, positive, unit
    # npr: {"1": [{"name": "gledanje tv", "total": 120, "positive": False, "unit": "minutes"}, {...}], "2": {...} itd...}

    year = data["year"]
    month = data["month"] + 1

    def checkDateMonth(date):
        return date.year == year and date.month == month
    
    def checkGoal(date, date_created, date_deleted, days):
        return days[date.weekday()] and date >= date_created and (date_deleted is True or date < date_deleted) and realToday != date

    logs = [l for l in action_log_table.search(query.username == user["username"]) if checkDateMonth(datetime.strptime(l["time"], "%Y-%m-%d %H:%M:%S").date())]

    history = {}

    realToday = datetime.now().date()
    monthLength = calendar.monthrange(year, month)[1]
    for day in range(1, monthLength + 1):
        # mamo year, month, day
        thisDate = dateObj(year, month, day)
        if(thisDate > realToday): break

        logsThisDay = [l for l in logs if datetime.strptime(l["time"], "%Y-%m-%d %H:%M:%S").date() == thisDate]

        allValid = []

        for g in goal_table.search(query.username == user["username"]):
            if not checkGoal(thisDate, datetime.strptime(g["date_created"], "%Y-%m-%d %H:%M:%S").date(), not g["date_deleted"] or datetime.strptime(g["date_deleted"], "%Y-%m-%d %H:%M:%S").date(), g["days"]): continue
            
            goal_unit = "amount" if g["amount"] else "duration_minutes"
            goal_action = actions_table.search((query.id == g["action_id"]) & (query.username == user["username"]))[0]

            full = 0
            for l in logsThisDay:
                if l["action_id"] == goal_action["id"]:
                    full += l[goal_unit] # problem: glej route check_goals_today; opisano tm
            
            allValid.append({"name": goal_action["name"], "total": full, "goal": g[goal_unit], "unit": goal_unit, "positive": g["positive"]})

        history[day] = allValid

    return jsonify({"status": "success", "history": history})



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


