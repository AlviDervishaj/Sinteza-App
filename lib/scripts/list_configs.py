import os
import sys

# go into accounts/{username} folder
# list all the files that end with .yml
# print the names of files

username: str = sys.argv[1]
configs = []
os.chdir(f"accounts/{username}")
for item in os.listdir():
    if not os.path.isdir(item):
        if item.endswith(".yml") and not (
            item.startswith("filters") or item.startswith("telegram")
        ):
            configs.append(item)


print(configs)
