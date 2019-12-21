class User:
    def __init__(self, data):
        self.id = data.get("id")
        self.username = data.get("username")
        self.email = data.get("email")
        self.password = data.get("password")
        self.name = data.get("name")
        self.surname = data.get("surname")
        self.age = data.get("age")
        self.ts_last_login = data.get("ts_last_login")
        self.ts_registration = data.get("ts_registration")
        self.registration_ip = data.get("registration_ip")
        self.last_login_ip = data.get("last_login_ip")

    def jwt_payload(self):
        return {
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
            "age": self.age,
            "ts_registration": self.ts_registration,
            "last_login_ip": self.last_login_ip
        }
