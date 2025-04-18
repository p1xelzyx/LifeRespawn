import uuid

class UserStateManager:
    def __init__(self):
        self.users = {}

    def login_user(self, user):
        id = str(uuid.uuid4())
        while id in self.users.values():
            id = str(uuid.uuid4())
        self.users[user] = id
    
    def logout_user(self, user):
        if user in self.users:
            self.users.pop(user)

    def get_user(self, id):
        return list(self.users.keys())[list(self.users.values()).index(id)]