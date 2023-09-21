import json
from datetime import date

today = date.today()

def extract_usernames(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    usernames_followed = []
    
    for username, user_info in data.items():
        date = int(user_info["last_interaction"].split(" ")[0].split("-")[2])
        month = int(user_info["last_interaction"].split(" ")[0].split("-")[1])
        tmonth = int(today.strftime("%m"))
        tDate = int(today.strftime("%d"))
        if user_info['following_status'] == "followed":
            if tmonth > month:
                usernames_followed.append(username)
            elif tDate > date + 4 and tmonth == month:
                usernames_followed.append(username)
            
    return usernames_followed


# Usage
file_path = 'interacted_users.json'
usernames = extract_usernames(file_path)

# Write the usernames to a file.
with open('followed_usernames.txt', 'w') as outfile:
    for username in usernames:
        outfile.write(username + '\n')