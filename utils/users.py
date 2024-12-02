from utils.config import load_config

async def user_is_admin(user_id=None, username=None):
    config = load_config()
    admins = config.get('admins', [])
    if username in admins:
        return True
    if user_id in admins:
        return True
    return False
    