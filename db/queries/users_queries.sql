-- CREATE

def create_new_user_query():
-- docustring meant to help you understand the purpose of this function
    """
    Returns the SQL query to insert a new user into the users table.
    """
    return """
    INSERT INTO users (username, email, password_hash, created_at, updated_at)
    VALUES (%s, %s, %s, NOW(), NOW());
    """

-- READ

def get_all_users_query():
    """
    Returns the SQL query to select all users from the users table.
    """
    return """
    SELECT * FROM users;
    """

def get_user_by_id_query():
    """
    Returns the SQL query to select a user by their ID from the users table.
    """
    return """
    SELECT * FROM users WHERE id = %s;
    """

def get_user_by_username_query():
    """
    Returns the SQL query to select a user by their username from the users table.
    """
    return """
    SELECT * FROM users WHERE username = %s;
    """

def get_user_by_email_query():
    """
    Returns the SQL query to select a user by their email from the users table.
    """
    return """
    SELECT * FROM users WHERE email = %s;
    """

def get_newest_users_query():
    """
    Returns the SQL query to select the newest users from the users table.
    """
    return """
    SELECT * FROM users ORDER BY created_at DESC LIMIT 10;
    """

-- UPDATE

def update_user_query(email_change, password_hash_change, user_id):
    """
    Returns the SQL query to update a user's email and/or password hash by their ID depending on what the user wants to change.
    """
    if email_change and password_hash_change:
        return """
        UPDATE users
        SET email = %s, password_hash = %s, updated_at = NOW()
        WHERE id = %s;
        """
    elif email_change:
        return """
        UPDATE users
        SET email = %s, updated_at = NOW()
        WHERE id = %s;
        """
    elif password_hash_change:
        return """
        UPDATE users
        SET password_hash = %s, updated_at = NOW()
        WHERE id = %s;
        """
    else:
        return None

-- DELETE

def delete_user_query():
    """
    Returns the SQL query to delete a user by their ID from the users table.
    """
    return """
    DELETE FROM users WHERE id = %s;
    """