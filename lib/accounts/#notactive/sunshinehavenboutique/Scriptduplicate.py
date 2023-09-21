import random

def find_duplicates(file1, file2, output_file):
    with open(file1, 'r') as f:
        usernames1 = set(line.strip() for line in f)
    with open(file2, 'r') as f:
        usernames2 = set(line.strip() for line in f)

    duplicates = usernames1 & usernames2
    unique_usernames1 = usernames1 - usernames2

    # Convert to list for random selection
    duplicates = list(duplicates)
    unique_usernames1 = list(unique_usernames1)
    
    with open(output_file, 'w') as f:
        for username in duplicates:
            f.write(username + '\n')
            for _ in range(random.randint(1, 3)):
                if unique_usernames1:  # check if there are still unique usernames left
                    unique_username = random.choice(unique_usernames1)
                    f.write(unique_username + '\n')
                    unique_usernames1.remove(unique_username)


# Usage
find_duplicates('followed_usernames.txt', 'followback_usernames.txt', 'duplicates.txt')
