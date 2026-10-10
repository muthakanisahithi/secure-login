import hashlib
import json
import os
from getpass import getpass

USERS_FILE = "users.json"
MAX_ATTEMPTS = 3


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE) as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000).hex()


def register():
    users = load_users()
    username = input("Choose username: ").strip()
    if username in users:
        print("Username already exists.")
        return
    password = getpass("Choose password: ")
    role = input("Role (admin/user): ").strip().lower()
    if role not in ("admin", "user"):
        print("Invalid role.")
        return
    salt = os.urandom(16)
    users[username] = {
        "salt": salt.hex(),
        "hash": hash_password(password, salt),
        "role": role,
        "failed": 0,
        "locked": False,
    }
    save_users(users)
    print("Registered successfully.")


def login():
    users = load_users()
    username = input("Username: ").strip()
    if username not in users:
        print("Invalid username or password.")
        return None
    user = users[username]
    if user["locked"]:
        print("Account is locked.")
        return None
    password = getpass("Password: ")
    salt = bytes.fromhex(user["salt"])
    if hash_password(password, salt) == user["hash"]:
        user["failed"] = 0
        save_users(users)
        print("Login successful.")
        return username, user["role"]
    user["failed"] += 1
    if user["failed"] >= MAX_ATTEMPTS:
        user["locked"] = True
        print("Too many wrong attempts. Account locked.")
    else:
        print(f"Wrong password. Attempts left: {MAX_ATTEMPTS - user['failed']}")
    save_users(users)
    return None


def admin_menu(username):
    print(f"\nWelcome admin {username}")
    users = load_users()
    print("All users:")
    for name, data in users.items():
        status = "LOCKED" if data["locked"] else "active"
        print(f"  {name} ({data['role']}) - {status}")


def user_menu(username):
    print(f"\nWelcome {username}. You have normal user access.")


def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            register()
        elif choice == "2":
            result = login()
            if result:
                username, role = result
                if role == "admin":
                    admin_menu(username)
                else:
                    user_menu(username)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


main()