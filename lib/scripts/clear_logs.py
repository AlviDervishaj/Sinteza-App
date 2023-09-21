import sys


username: str = sys.argv[1]

path: str = f"logs/{username}.log"

with open(path, "w") as file:
    file.write("")


