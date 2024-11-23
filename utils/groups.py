from utils.settings import load_settings, save_settings

def add_group(group_name: str) -> bool:
    settings = load_settings()
    groups = settings.get("groups", [])
    groups.append(group_name)
    save_settings(settings)
    return True

def delete_group(group_name: str) -> bool:
    settings = load_settings()
    groups = settings.get("groups", [])

    if group_name in groups:
        groups.remove(group_name)
        settings["groups"] = groups
        save_settings(settings)
        return True
    return False

def list_groups():
    settings = load_settings()
    return settings.get("groups", [])
