import mysql.connector
from mysql.connector import Error


def stream_users():
    """Generator that yields rows from user_data table one by one as dict"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # ← Update if needed
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Database error: {e}")
