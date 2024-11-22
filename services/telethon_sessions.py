import os
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from dotenv import load_dotenv
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_FOLDER = "sessions"

def ensure_session_folder():
    if not os.path.exists(SESSION_FOLDER):
        os.makedirs(SESSION_FOLDER)

async def create_telethon_session(phone: str):
    ensure_session_folder()
    session_path = os.path.join(SESSION_FOLDER, f"{phone}.session")
    
    client = TelegramClient(session_path, API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            print(f"Код подтверждения отправлен на номер {phone}.")
            code = input("Введите код подтверждения: ")
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            password = input("Введите пароль от двухфакторной аутентификации: ")
            await client.sign_in(password=password)
    
    print(f"Сессия для номера {phone} успешно создана.")
    return client
