import os
import re

GROUPS_FILE = 'groups.txt'

def list_groups():
    if not os.path.exists(GROUPS_FILE):
        return []
    with open(GROUPS_FILE, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]

def add_group(group_name):
    if not os.path.exists(GROUPS_FILE):
        open(GROUPS_FILE, 'w', encoding='utf-8').close()

    with open(GROUPS_FILE, 'a', encoding='utf-8') as f:
        f.write(group_name + "\n")

def validate_group_link(group_link):
    pattern = r"^t.me/[a-zA-Z0-9_]+$"
    return re.match(pattern, group_link) is not None

def delete_group(group_name):
    if not os.path.exists(GROUPS_FILE):
        return False

    with open(GROUPS_FILE, 'r', encoding='utf-8') as f:
        groups = [line.strip() for line in f.readlines()]

    if group_name in groups:
        groups.remove(group_name)
        with open(GROUPS_FILE, 'w', encoding='utf-8') as f:
            f.writelines(group + '\n' for group in groups)
        return True
    return False

