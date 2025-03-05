import hashlib
from helpers.database import Database


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)
        self.logged_user = None

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self):
        db = Database()
        conn = db.connect_database()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT username, role FROM users WHERE username=%s AND password=%s",
                           (self.username, self.password))
            user = cursor.fetchone()
            if user:
                self.logged_user = user[0]
                print(f"\nUser: {self.username} logged in successfully.")
                return True
            return False

        except Exception as e:
            print(f"Authentication Error: {e}")
            return False

        finally:
            db.close()
