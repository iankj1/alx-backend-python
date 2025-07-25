# Task 0: Getting Started with Python Generators

This task sets up a MySQL database using Python, creates a `user_data` table, and populates it with values from a CSV file using basic MySQL connector logic.

### Files

- `seed.py`: Contains logic for connecting to the database, creating tables, and inserting data.
- `user_data.csv`: CSV file with sample user data.
- `0-main.py`: Test runner to check if database and table creation, and data insertion works correctly.

### Functions

- `connect_db()`: Connects to MySQL server.
- `create_database(connection)`: Creates the `ALX_prodev` database.
- `connect_to_prodev()`: Connects to `ALX_prodev`.
- `create_table(connection)`: Creates the `user_data` table.
- `insert_data(connection, 'user_data.csv')`: Loads user records from CSV into the table.
