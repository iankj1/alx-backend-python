import mysql.connector
import csv
from mysql.connector import Error


def connect_db():
    """Connect to MySQL server (without selecting a DB)"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""  # ← Replace with your MySQL password if needed
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Create ALX_prodev database if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connect to the ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # ← Replace with your MySQL password if needed
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Create the user_data table"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            );
        """)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, data_file):
    """Insert CSV data into the user_data table"""
    try:
        cursor = connection.cursor()
        with open(data_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check if the user already exists
                cursor.execute("SELECT COUNT(*) FROM user_data WHERE user_id = %s;", (row['user_id'],))
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s);
                    """, (row['user_id'], row['name'], row['email'], row['age']))
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print("CSV file not found.")
