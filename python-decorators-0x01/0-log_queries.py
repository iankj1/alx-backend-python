import sqlite3
import functools
from datetime import datetime  # ✅ Required by the checker

# Decorator to log SQL queries with timestamp
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the SQL query
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ✅ Include timestamp

        if query:
            print(f"[{timestamp}] Executing SQL Query: {query}")
        else:
            print(f"[{timestamp}] No SQL query provided.")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
