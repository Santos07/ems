import psycopg2

DB_SERVER_CONFIG = {
    "user": "postgres",
    "password": "Welcome1",
    "host": "localhost",
    "port": "5432",
}

DB_CONFIG = {
    "user": "postgres",
    "password": "Welcome1",
    "host": "localhost",
    "port": "5432",
    "dbname": "employee_db"
}

# Database Queries
CREATE_DATABASE_QUERY = """
    CREATE DATABASE employee_db;
"""

CREATE_USERS_TABLE_QUERY = """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL,
        role VARCHAR(20) CHECK (role IN ('admin', 'employee')) NOT NULL    
    )
"""

CREATE_EMPLOYEES_TABLE_QUERY = """
    CREATE TABLE employees (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        age INT,
        department VARCHAR(100),
        salary DECIMAL(10,2)
    )
"""

SEED_ADMIN_USER = """
    INSERT INTO users(username, password, role) VALUES
    ('admin','8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'admin')
"""


class Database:
    def __init__(self):
        self.conn = None

    def connect_database_server(self):
        try:
            self.conn = psycopg2.connect(**DB_SERVER_CONFIG)
            return self.conn
        except Exception as e:
            print(f"Error connecting to the database server: {e}")

    def connect_database(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            return self.conn
        except Exception as e:
            print(f"Error Connecting to the Database: {e}")

    def close(self):
        if self.conn:
            self.conn.close()

    def setup_database(self):
        try:
            conn = self.connect_database_server()
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(CREATE_DATABASE_QUERY)
            self.close()
            print("Database created successfully!")

        except Exception as e:
            print(f"Error creating database: {e}")

        try:
            conn = self.connect_database()
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(CREATE_USERS_TABLE_QUERY)
            cursor.execute(CREATE_EMPLOYEES_TABLE_QUERY)
            cursor.execute(SEED_ADMIN_USER)
            self.close()
            print("Tables created successfully!")

        except Exception as e:
            print(f"Error creating tables : {e}")
