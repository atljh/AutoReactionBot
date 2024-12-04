import os
from telethon import TelegramClient
from utils.config import load_config
from utils.console import console

SESSION_FOLDER = "sessions"

config = load_config()

def list_sessions():
    """
    Возвращает список всех файлов сессий в папке.
    """
    if not os.path.exists(SESSION_FOLDER):
        return []
    return [f.replace(".session", "") for f in os.listdir(SESSION_FOLDER) if f.endswith(".session")]


async def get_account_info(phone: str):
    """
    Получает информацию об аккаунте из сессии.
    
    :param phone: Номер телефона или имя файла сессии.
    :return: Словарь с информацией об аккаунте.
    """
    session_path = os.path.join(SESSION_FOLDER, f"{phone}.session")
    if not os.path.exists(session_path):
        return None

    client = TelegramClient(
        session_path, config.get("api_id"), config.get("api_hash")
    )
    try:
        await client.connect()
    except Exception as e:
        console.log(f"Error phone {phone}", e)
        return None
        
    if not await client.is_user_authorized():
        await client.disconnect()
        return None

    user = await client.get_me()
    await client.disconnect()

    return {
        "id": user.id,
        "phone": user.phone,
        "username": user.username or "Без имени пользователя",
        "first_name": user.first_name or "Без имени",
        "last_name": user.last_name or "",
    }
