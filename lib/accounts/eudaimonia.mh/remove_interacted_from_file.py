import os
import json


def logger(x):
    return print(x, flush=True)


# format: usernameToBeKept,account
with open("keep_usernames.txt", "r") as f:
    data = f.read().split("\n")

# get usernames
folders = []

username = os.getcwd().split("\\")[-1]
logger(f"Username: {username}")

if not os.path.isfile("interacted_users.json"):
    logger(f"Could not find interacted_users.json in {username}")

with open("interacted_users.json", "r") as f:
    interacted_users = json.load(f)


# loop over keys
temp = interacted_users.copy()
for key in temp.keys():
    if key in data:
        logger(f"Found {key} in keep_usernames.txt")
        continue
    else:
        logger(f"Deleting {key}")
        del interacted_users[key]


with open("interacted_users.json", "w") as f:
    json.dump(interacted_users, f, indent=4)
