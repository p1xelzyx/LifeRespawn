from tinydb import TinyDB, Query
from datetime import datetime, timedelta, date, time
import random
import math

db = TinyDB('../db.json')
user_table = db.table("users")
actions_table = db.table("actions")
action_log_table = db.table("action_logs")
mood_log_table = db.table("mood_logs")
goal_table = db.table("goals")
mission_table = db.table("missions")
query = Query()

def new_id(sez):
    min_id = 0
    for e in sez:
        if e["id"] > min_id: 
            min_id = e["id"]
    return min_id + 1
def random_centered_on_6_5():
    # Box-Muller transform to get standard normal (mean = 0, stddev = 1)
    u1, u2 = random.random(), random.random()
    z = ( (-2 * math.log(u1)) ** 0.5 ) * math.cos(2 * math.pi * u2)

    # Scale and shift: mean = 6.5, stddev = 1 (adjust as needed)
    mean = 6.5
    stddev = 1.0
    value = z * stddev + mean

    # Clamp to [1, 10]
    return max(1, min(10, value))


from datetime import date, timedelta

# Define start and end dates
start_date = date(2024, 1, 1)
end_date = date(2025, 5, 25)

# 1, zlo dobr (fitnes), 2 zlo slabo (instagram), 5 dobr (meditation)



# Loop through dates
current_date = start_date
while current_date <= end_date:
    #print(current_date)
    actionsLogs = [l for l in action_log_table.all() if datetime.strptime(l["time"], "%Y-%m-%d %H:%M:%S").date() == current_date]

    val = random_centered_on_6_5()

    dt = datetime.combine(current_date, time(1, 0, 0))

    # Format as string
    formatted = dt.strftime("%Y-%m-%d %H:%M:%S")


    jeFitnes = 0
    jeInsta = 0
    jeMeditation = 0
    for l in actionsLogs:
        if l["action_id"] == 1:
            jeFitnes = 1
        if l["action_id"] == 2:
            jeInsta = 1
        if l["action_id"] == 5:
            jeMeditation = 1
    
    dif = 0
    if jeFitnes + jeMeditation == 1:
        dif += 1
    if jeMeditation and jeMeditation:
        dif += 1.5
    if jeInsta:
        dif -= 1

    #print("------------------ ", current_date, " ----------------------")
    #print("fitnes: ", jeFitnes)
    #print("meditation: ", jeMeditation)
    #print("insta: ", jeInsta)
    #print(dif)
    



    toIn = {"id": new_id(mood_log_table.all()), "mood": max(min(math.floor((val + dif) * 10) / 10, 10), 0), "time": formatted, "username": "test"}
    print(toIn)
    mood_log_table.insert(toIn)
    
    current_date += timedelta(days=1)