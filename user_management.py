# user_management.py

import csv
import os
import bcrypt
from typing import List, Dict

# Path to the approved_user_list.csv file
USER_CSV_PATH = os.path.join("approved_user_list", "approved_user_list.csv")

def load_users() -> Dict[str, Dict]:
    """
    Loads users from the approved_user_list.csv file.

    Returns:
        Dict[str, Dict]: A dictionary of users with usernames as keys.
    """
    users = {}
    if not os.path.exists(USER_CSV_PATH):
        print(f"User CSV file not found: {USER_CSV_PATH}")
        return users  # Return empty dictionary if no file found

    with open(USER_CSV_PATH, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            username = row['username'].strip().lower()  # Normalize username
            if username:  # Ensure username is not empty
                users[username] = {
                    'id': row['id'],
                    'username': username,
                    'pin': row['pin'],  # This is the hashed PIN
                    'email': row['email'].strip(),
                    'role': row['role'].strip()
                }
            else:
                print("Skipping user with missing or empty username during load.")
    return users

def save_users(users: List[Dict]):
    """
    Saves the list of users back to the approved_user_list.csv file.

    Args:
        users (List[Dict]): A list of user dictionaries.
    """
    with open(USER_CSV_PATH, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'username', 'pin', 'email', 'role']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user in users:
            if 'username' in user and user['username'].strip():
                writer.writerow(user)
            else:
                print("Skipping user with missing or empty username during save.")

def hash_pin(pin: str) -> str:
    """
    Hashes a PIN using bcrypt.

    Args:
        pin (str): The plaintext PIN.

    Returns:
        str: The hashed PIN.
    """
    salt = bcrypt.gensalt()
    hashed_pin = bcrypt.hashpw(pin.encode('utf-8'), salt)
    return hashed_pin.decode('utf-8')

def verify_pin(pin: str, hashed_pin: str) -> bool:
    """
    Verifies a PIN against a hashed PIN.

    Args:
        pin (str): The plaintext PIN.
        hashed_pin (str): The hashed PIN.

    Returns:
        bool: True if the PIN matches the hash, False otherwise.
    """
    return bcrypt.checkpw(pin.encode('utf-8'), hashed_pin.encode('utf-8'))

def add_user(user_data: Dict) -> bool:
    """
    Adds a new user to the approved_user_list.csv file.

    Args:
        user_data (Dict): A dictionary containing new user information. Expected keys:
                          - id (str or int)
                          - username (str)
                          - pin (str)
                          - email (str)
                          - role (str)

    Returns:
        bool: True if the user was added successfully, False if the username already exists or data is incomplete.
    """
    users = load_users()

    username = user_data['username'].strip().lower()

    # Check if the username already exists (case-insensitive)
    if username in users:
        print(f"Add User Failed: Username '{username}' already exists.")
        return False  # Username already exists

    # Validate that all required fields are present
    required_fields = {'id', 'username', 'pin', 'email', 'role'}
    if not required_fields.issubset(user_data.keys()):
        print("Add User Failed: Missing required user fields.")
        return False  # Missing required fields

    # Hash the PIN before storing
    hashed_pin = hash_pin(user_data['pin'])

    # Prepare the new user data
    new_user = {
        "id": str(user_data['id']),
        "username": username,
        "pin": hashed_pin,
        "email": user_data['email'].strip(),
        "role": user_data['role'].strip()
    }

    # Append the new user
    users_list = list(users.values())
    users_list.append(new_user)
    save_users(users_list)
    print(f"User '{username}' added successfully.")
    return True

def reset_password(username: str, new_pin: str) -> bool:
    """
    Resets the password for an existing user.

    Args:
        username (str): The username of the user.
        new_pin (str): The new PIN to set.

    Returns:
        bool: True if the password was reset successfully, False otherwise.
    """
    users = load_users()
    username = username.strip().lower()
    user_found = False

    for user in users.values():
        if user['username'] == username:
            user['pin'] = hash_pin(new_pin)
            user_found = True
            break

    if user_found:
        save_users(list(users.values()))
        print(f"Password reset successfully for user '{username}'.")
        return True
    else:
        print(f"Reset Password Failed: User '{username}' not found.")
        return False
