from helpers.database import Database
from models.users import User


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    def add_user(self, new_username, new_password, role):
        db = Database()
        conn = db.connect_database()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            hashed_password = self.hash_password(new_password)
            new_user = cursor.execute("INSERT INTO users (username, password, role) VALUES (%s,%s,%s)",
                                      (new_username, hashed_password, role))
            print(f"User {new_username} added successfully")
            conn.commit()
            return new_user

        except Exception as e:
            print(f"Error adding user : {e}")
        finally:
            db.close()
