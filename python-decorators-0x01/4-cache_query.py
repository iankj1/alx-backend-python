import time
import sqlite3
import functools

query_cache = {}

# Decorator to provide a database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Decorator to cache query results based on query string
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract the query from args or kwargs
        query = kwargs.get('query') if 'query' in kwargs else args[1] if len(args) > 1 else None

        if query in query_cache:
            print("[CACHE] Returning cached result.")
            return query_cache[query]

        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        print("[CACHE] Caching new result.")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
