import json
from datetime import datetime

def main():
    # Get the file path from the user.
    file_path = "interacted_users.json"

    # Open the file in read mode.
    with open(file_path, "r") as file:
        data = json.load(file)

    # Get the input date from the user
    input_date_str = input("Enter a date (YYYY-MM-DD): ")
    input_date = datetime.strptime(input_date_str, "%Y-%m-%d")

    # Remove usernames with last_interaction older than input_date
    usernames_to_remove = [username for username, user_data in data.items() if datetime.strptime(user_data["last_interaction"], "%Y-%m-%d %H:%M:%S.%f") < input_date or user_data["following_status"] == "none"]
    for username in usernames_to_remove:
        del data[username]

    # Write back remaining usernames and their data to a file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    main()
