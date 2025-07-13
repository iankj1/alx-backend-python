import sqlite3

# Class-based context manager
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # Return the connection object

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()  # Ensure the connection is closed

# Use the context manager to query the users table
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
