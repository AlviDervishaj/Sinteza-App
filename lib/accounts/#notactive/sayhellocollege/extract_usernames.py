import json

def extract_usernames(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    usernames_followed = []
    
    for username, user_info in data.items():
        if user_info['following_status']=="followed":
            usernames_followed.append(username)
            
    return usernames_followed


# Usage
file_path = 'interacted_users.json'
usernames = extract_usernames(file_path)

# Write the usernames to a file.
with open('followed_usernames.txt', 'w') as outfile:
    for username in usernames:
        outfile.write(username + '\n')