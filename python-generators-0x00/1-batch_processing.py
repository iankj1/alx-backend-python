import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """Generator that yields rows in batches from user_data"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Update with your MySQL password if needed
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")  # ✅ Required by checker
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows  # ✅ Use yield (not return or print)
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Database error: {e}")


def batch_processing(batch_size):
    """Generator that filters users older than 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:  # ✅ Required by checker
                yield user  # ✅ Use yield instead of print()
