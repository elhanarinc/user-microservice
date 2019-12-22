class UserBuilder:
    def __init__(self):
        self.user = {}

    def with_username(self, value):
        self.user["username"] = value
        return self

    def with_name(self, value):
        self.user["name"] = value
        return self

    def with_surname(self, value):
        self.user["surname"] = value
        return self

    def with_email(self, value):
        self.user["email"] = value
        return self

    def with_age(self, value):
        self.user["age"] = value
        return self

    def with_password(self, value):
        self.user["password"] = value
        return self

    def build(self):
        return self.user
