import os

# go into accounts folder
# list all the directories / folders
# do not list files
# print the names of directories / folders

os.chdir("accounts")
users: list = []
for item in os.listdir():
    if os.path.isdir(item):
        users.append(item)

print(users)
