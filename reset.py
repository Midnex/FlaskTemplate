import os

db_path = os.path.join("instance", "database.db")

if os.path.exists(".env"):
    os.remove(".env")
    print("Deleted .env file.")
else:
    print(".env file not found.")

if os.path.exists(db_path):
    os.remove(db_path)
    print("Deleted database.db file.")
else:
    print("database.db not found.")
