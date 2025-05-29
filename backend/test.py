from tinydb import TinyDB, Query
from datetime import datetime, timedelta, date
import random
import calendar

# Initialize database
db = TinyDB('../db.json')
user_table = db.table("users")
actions_table = db.table("actions")
action_log_table = db.table("action_logs")
mood_log_table = db.table("mood_logs")
goal_table = db.table("goals")
mission_table = db.table("missions")
query = Query()

# Utility function to generate new IDs
def new_id(sez):
    min_id = 0
    for e in sez:
        if e["id"] > min_id: 
            min_id = e["id"]
    return min_id + 1

# Clean existing test user data (except the user itself)
def clean_existing_data():
    actions_table.remove(query.username == "test")
    action_log_table.remove(query.username == "test")
    mood_log_table.remove(query.username == "test")
    goal_table.remove(query.username == "test")
    mission_table.remove(query.username == "test")

# Create actions for test user
def create_actions():
    actions = [
        {"name": "Fitness", "impact": 3, "username": "test"},
        {"name": "Instagram", "impact": -2, "username": "test"},
        {"name": "TV", "impact": -3, "username": "test"},
        {"name": "Learning", "impact": 4, "username": "test"},
        {"name": "Meditation", "impact": 2, "username": "test"},
        {"name": "Reading", "impact": 1, "username": "test"},
        {"name": "Cooking", "impact": 1, "username": "test"},
    ]
    
    # Get next available ID
    next_id = new_id(actions_table.all())
    
    # Insert actions and store their IDs
    action_ids = []
    for action in actions:
        action["id"] = next_id
        actions_table.insert(action)
        action_ids.append(next_id)
        next_id += 1
        
    return action_ids

# Create goals for test user
def create_goals(action_ids):
    fitness_id, insta_id, tv_id, learning_id, meditation_id, _, _ = action_ids
    
    # Get creation date (16 months ago)
    creation_date = (datetime.now() - timedelta(days=16*30)).strftime("%Y-%m-%d %H:%M:%S")
    
    goals = [
        # Fitness - positive duration goal (Mon-Fri)
        {
            "action_id": fitness_id,
            "duration_minutes": 60,
            "amount": False,
            "positive": True,
            "days": [1, 1, 1, 1, 1, 0, 0],
            "date_created": creation_date,
            "date_deleted": False,
            "username": "test"
        },
        # Instagram - negative duration goal (daily)
        {
            "action_id": insta_id,
            "duration_minutes": 30,
            "amount": False,
            "positive": False,
            "days": [1, 1, 1, 1, 1, 1, 1],
            "date_created": creation_date,
            "date_deleted": False,
            "username": "test"
        },
        # TV - negative duration goal (deleted after 8 months)
        {
            "action_id": tv_id,
            "duration_minutes": 60,
            "amount": False,
            "positive": False,
            "days": [1, 1, 1, 1, 1, 1, 1],
            "date_created": creation_date,
            "date_deleted": (datetime.now() - timedelta(days=8*30)).strftime("%Y-%m-%d %H:%M:%S"),
            "username": "test"
        },
        # Learning - positive duration goal (Mon-Thu)
        {
            "action_id": learning_id,
            "duration_minutes": 120,
            "amount": False,
            "positive": True,
            "days": [1, 1, 1, 1, 0, 0, 0],
            "date_created": creation_date,
            "date_deleted": False,
            "username": "test"
        },
        # Meditation - positive amount goal (deleted after 4 months)
        {
            "action_id": meditation_id,
            "duration_minutes": False,
            "amount": 1,
            "positive": True,
            "days": [1, 1, 1, 1, 1, 1, 1],
            "date_created": creation_date,
            "date_deleted": (datetime.now() - timedelta(days=4*30)).strftime("%Y-%m-%d %H:%M:%S"),
            "username": "test"
        }
    ]
    
    # Get next available ID
    next_id = new_id(goal_table.all())
    
    # Insert goals
    for goal in goals:
        goal["id"] = next_id
        goal_table.insert(goal)
        next_id += 1

# Generate action logs with correlations
def generate_action_logs(action_ids, start_date, end_date):
    fitness_id, insta_id, tv_id, learning_id, meditation_id, reading_id, cooking_id = action_ids
    
    current_date = start_date
    day_count = (end_date - start_date).days
    
    for day in range(day_count + 1):
        date = start_date + timedelta(days=day)
        date_str = date.strftime("%Y-%m-%d %H:%M:%S")
        weekday = date.weekday()
        
        # Skip 10% of days completely
        if random.random() < 0.1:
            continue
            
        # Create logs for each action type
        actions = []
        
        # Fitness - more likely on weekdays
        if weekday < 5 and random.random() < 0.8:  # 80% chance on weekdays
            actions.append({
                "action_id": fitness_id,
                "duration_minutes": random.randint(30, 90),
                "amount": 0
            })
        
        # Instagram - daily but with random usage
        if random.random() < 0.9:  # 90% chance daily
            actions.append({
                "action_id": insta_id,
                "duration_minutes": random.randint(5, 120),
                "amount": 0
            })
        
        # TV - daily but with random usage
        if random.random() < 0.7:  # 70% chance daily
            actions.append({
                "action_id": tv_id,
                "duration_minutes": random.randint(30, 180),
                "amount": 0
            })
        
        # Learning - mostly on weekdays
        if weekday < 4 and random.random() < 0.7:  # 70% chance Mon-Thu
            actions.append({
                "action_id": learning_id,
                "duration_minutes": random.randint(60, 180),
                "amount": 0
            })
        
        # Meditation - daily practice
        if random.random() < 0.6:  # 60% chance daily
            actions.append({
                "action_id": meditation_id,
                "duration_minutes": 0,
                "amount": 1
            })
        
        # Additional actions without goals
        if random.random() < 0.4:  # 40% chance
            actions.append({
                "action_id": reading_id,
                "duration_minutes": random.randint(15, 60),
                "amount": 0
            })
        
        if random.random() < 0.3:  # 30% chance
            actions.append({
                "action_id": cooking_id,
                "duration_minutes": random.randint(20, 60),
                "amount": 0
            })
        
        # Special patterns
        # Complete all goals for a week (every 2 months)
        if day % 60 < 7:  
            actions = [
                {"action_id": fitness_id, "duration_minutes": 60, "amount": 0},
                {"action_id": insta_id, "duration_minutes": 20, "amount": 0},
                {"action_id": tv_id, "duration_minutes": 45, "amount": 0},
                {"action_id": learning_id, "duration_minutes": 120, "amount": 0},
                {"action_id": meditation_id, "duration_minutes": 0, "amount": 1}
            ]
        
        # No actions for a week (every 3 months)
        elif day % 90 < 7:  
            actions = []
        
        # Insert action logs
        next_id = new_id(action_log_table.all())
        for action in actions:
            action_log_table.insert({
                "id": next_id,
                "action_id": action["action_id"],
                "duration_minutes": action["duration_minutes"],
                "amount": action["amount"],
                "time": date_str,
                "username": "test"
            })
            next_id += 1

# Generate mood logs (1-10 scale) with correlations
def generate_mood_logs(start_date, end_date):
    day_count = (end_date - start_date).days
    
    for day in range(day_count + 1):
        date = start_date + timedelta(days=day)
        date_str = date.strftime("%Y-%m-%d %H:%M:%S")
        
        # Get actions for this day to influence mood
        logs = action_log_table.search(
            (query.time.startswith(date.strftime("%Y-%m-%d"))) & 
            (query.username == "test")
        )
        
        # Calculate base mood (5-7) with action influences
        base_mood = random.randint(5, 7)
        
        # Positive correlation with fitness
        if any(log["action_id"] == fitness_id for log in logs):
            base_mood += random.randint(1, 3)
        
        # Negative correlations
        insta_time = sum(log["duration_minutes"] for log in logs if log["action_id"] == insta_id)
        tv_time = sum(log["duration_minutes"] for log in logs if log["action_id"] == tv_id)
        
        if insta_time > 60:
            base_mood -= random.randint(1, 2)
        if tv_time > 90:
            base_mood -= random.randint(1, 3)
        
        # Generate 1-4 mood logs per day
        num_logs = random.randint(1, 4)
        
        for _ in range(num_logs):
            # Add time variation
            hour = random.randint(7, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            
            log_time = datetime(
                date.year, 
                date.month, 
                date.day,
                hour, minute, second
            ).strftime("%Y-%m-%d %H:%M:%S")
            
            # Calculate final mood with some randomness
            final_mood = base_mood + random.uniform(-1.5, 1.5)
            final_mood = max(1, min(10, int(round(final_mood))))
            
            # Insert mood log
            mood_log_table.insert({
                "id": new_id(mood_log_table.all()),
                "mood": final_mood,
                "time": log_time,
                "username": "test"
            })

# Create missions for test user
def create_missions():
    missions = [
        {"name": "Complete fitness challenge", "description": "Exercise 5 days this week", "priority": 2, "completed": 0, "username": "test"},
        {"name": "Limit social media", "description": "Stay under 30 mins/day for Instagram", "priority": 1, "completed": 1, "username": "test"},
        {"name": "Learn new skill", "description": "Complete 4 learning sessions", "priority": 2, "completed": 0, "username": "test"},
        {"name": "Meditation streak", "description": "Meditate for 7 days straight", "priority": 1, "completed": -1, "username": "test"},
        {"name": "Cook healthy meals", "description": "Prepare 3 healthy dinners", "priority": 0, "completed": 0, "username": "test"}
    ]
    
    next_id = new_id(mission_table.all())
    for mission in missions:
        mission["id"] = next_id
        mission_table.insert(mission)
        next_id += 1

# Main function
def main():
    # Clean existing test user data
    clean_existing_data()
    
    # Create actions and get their IDs
    action_ids = create_actions()
    global fitness_id, insta_id, tv_id
    fitness_id, insta_id, tv_id, _, _, _, _ = action_ids
    
    # Create goals
    create_goals(action_ids)
    
    # Generate data for last 16 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=16*30)  # Approx 16 months
    
    # Generate action logs
    generate_action_logs(action_ids, start_date.date(), end_date.date())
    
    # Generate mood logs (1-10 scale)
    generate_mood_logs(start_date.date(), end_date.date())
    
    # Create missions
    create_missions()
    
    print("Successfully generated test data for 'test' user!")

if __name__ == "__main__":
    main()