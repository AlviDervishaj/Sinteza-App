import sys
import os
import json

username = str(sys.argv[1])

file_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "accounts",
    username,
    "interacted_users.json",
)

with open(file_path, "r") as f:
    interacted_users: dict = json.load(f)

# Get all the usernames
interacted_users_list = list(interacted_users.keys())
print(interacted_users_list, flush=True)
