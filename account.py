class Account:
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def __str__(self):
        return f"Account(name='{self.name}', username='{self.username}', password='{'*' * len(self.password)}')"

    def to_dict(self):
        return {"name": self.name, "username": self.username, "password": self.password}

    @staticmethod
    def from_dict(data):
        return Account(data["name"], data["username"], data["password"])
