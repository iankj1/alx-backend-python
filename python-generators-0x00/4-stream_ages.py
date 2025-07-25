import mysql.connector
from mysql.connector import Error


def stream_user_ages():
    """Generator to stream user ages one by one from user_data"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  #  Update this if needed
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data;")
        for (age,) in cursor:
            yield age
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Database error: {e}")


def compute_average_age():
    """Computes and prints the average age using the generator"""
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    if count > 0:
        avg = total / count
        print(f"Average age of users: {avg}")
    else:
        print("No user data found.")
