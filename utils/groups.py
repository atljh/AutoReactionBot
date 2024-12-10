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

def delete_group(group: str) -> bool:
    settings = load_settings()
    groups = settings.get("groups", {})
    active_groups = settings.get("active_groups", [])

    if group in groups:
        del groups[group]
        settings["groups"] = groups
        if group in active_groups:
            active_groups.remove(group)
        save_settings(settings)
        return True
    return False 

def list_groups():
    settings = load_settings()
    return settings.get("groups", {})


def get_account_groups(account):
    """
    Возвращает список групп, к которым привязан указанный аккаунт.

    :param account: Номер телефона аккаунта (например, "+38093531234").
    :return: Список ссылок на группы.
    """
    settings = load_settings()
    groups = settings.get("groups", {})
    
    account_groups = [group for group, accounts in groups.items() if account in accounts]
    return account_groups


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

def unlink_account_from_group(account, group):
    settings = load_settings()
    if group in settings.get("groups", {}) and account in settings["groups"][group]:
        settings["groups"][group].remove(account)
        save_settings(settings)
        return True
    return False

def is_group_active(group):
    settings = load_settings()
    active_groups = settings.get("active_groups", [])
    if group in active_groups:
        return True
    return False

def get_active_groups():
    settings = load_settings()
    active_groups = settings.get("active_groups", [])
    return active_groups if len(active_groups) else None


def get_active_group_accounts(group):
    """
    Получить список аккаунтов, привязанных к активной группе.
    
    Args:
        group (str): Название или идентификатор группы.
    
    Returns:
        list: Список аккаунтов, привязанных к указанной группе.
    """
    settings = load_settings()
    groups = settings.get("groups", {})
    
    if group in groups:
        return groups[group]
    
    return []



def set_active_group(group):
    settings = load_settings()
    active_groups = settings.get("active_groups", [])
    active_groups.append(group)
    save_settings(settings)

def delete_active_group(group):
    settings = load_settings()
    active_groups = settings["active_groups"]
    if group in active_groups:
        active_groups.remove(group)
        save_settings(settings)
        return True
    return False
