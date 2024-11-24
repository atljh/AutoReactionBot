from utils.settings import load_settings, save_settings

def add_group(group_name: str) -> bool:
    settings = load_settings()
    groups = settings.get("groups", [])
    if group_name.startswith('t.me/'):
        groups.append(group_name)
    else:
        groups.append(int(group_name))
    save_settings(settings)
    return True

def delete_group(group_identifier) -> bool:

    settings = load_settings()
    groups = settings.get("groups", [])
    
    if isinstance(group_identifier, int):
        group_identifier = str(group_identifier)
    
    for i, group in enumerate(groups):
        if str(group) == group_identifier:
            del groups[i]
            settings["groups"] = groups
            save_settings(settings)
            return True

    return False


def list_groups():
    settings = load_settings()
    return settings.get("groups", [])
