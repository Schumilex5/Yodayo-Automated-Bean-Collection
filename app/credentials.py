# Username and Password pairs
credential_list = []

with open("../users.txt", "r") as file:
    lines = file.readlines()
    total_lines = len(lines)

    for i in range(0, total_lines, 3):
        email = lines[i].strip()
        password = lines[i+1].strip()
        credential_list.append((email, password))
