class User():
    def __init__(self, userID, name, user_name, email, passwort):
        self.userID = userID
        self.name = name
        self.user_name = user_name
        self.email = email
        self.passwort = passwort


class AdminUser():
    def __init__(self, userID, name, user_name, email, passwort):
        self.userID = userID
        self.name = name
        self.user_name = user_name
        self.email = email
        self.passwort = passwort

    def cancel_reservation(self):
        return True
