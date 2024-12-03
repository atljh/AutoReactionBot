from utils.config import load_config, save_config, update_config

async def user_is_admin(user_id=None, username=None):
    config = load_config()
    admins = config.get('admins', [])
    if username in admins:
        return True
    if user_id in admins:
        return True
    return False
    
def add_admin_to_config(admin: str):
    config = load_config()
    if admin.startswith("@"):
        admin = admin.replace("@", '')
    admins = config.get('admins', [])
    if admin.isdigit():
        admins.append(int(admin))
    else:
        admins.append(admin)
    config['admins'] = admins
    update_config('admins', admins)        
    
def delete_admin_from_config(admin: str):
    config = load_config()
    if admin.startswith("@"):
        admin = admin.replace("@", '')
    if admin.isdigit():
        admin = int(admin)
    admins = config.get('admins', [])
    if not admin in admins:
        return False
    admins.remove(admin)
    config['admins'] = admins
    update_config('admins', admins)
    return True