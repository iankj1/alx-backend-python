seed = __import__('seed')


def paginate_users(page_size, offset):
    """Fetch a page of users from the database using LIMIT and OFFSET."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """Generator that lazily loads paginated user data."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page  #  Yield each page of users
        offset += page_size  # Move to next page
