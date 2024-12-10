import json

from utils.settings import load_settings, save_settings

def add_group(group_name: str) -> bool:
    settings = load_settings()
    groups = settings.get("groups", {})
    if group_name not in groups:
        groups[group_name] = [] 
        settings["groups"] = groups
        save_settings(settings)
        return True
    return False 

def delete_group(group_identifier: str) -> bool:
    settings = load_settings()
    groups = settings.get("groups", {})
    
    if group_identifier in groups:
        del groups[group_identifier]
        settings["groups"] = groups
        save_settings(settings)
        return True
    return False 

def list_groups():
    settings = load_settings()
    return settings.get("groups", {})


def link_account_to_group(group, account):
    try:
        with open("settings.json", "r") as file:
            data = json.load(file)

        if group not in data["groups"]:
            return False 
        
        if "groups" not in data:
            data["groups"] = {}
        
        if group not in data["groups"]:
            data["groups"][group] = []
        
        if account not in data["groups"][group]:
            if len(data["groups"][group]) < 3: 
                data["groups"][group].append(account)
            else:
                return False
        with open("settings.json", "w") as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False