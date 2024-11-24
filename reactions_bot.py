import os
import asyncio
import json
from random import choice, randint
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.errors.rpcerrorlist import ChatAdminRequiredError

SESSION_FOLDER = "sessions"
os.makedirs(SESSION_FOLDER, exist_ok=True)

SETTINGS_FILE = "settings.json"

async def load_settings():
    """
    Загрузка настроек из settings.json.
    """
    if not os.path.exists(SETTINGS_FILE):
        print(f"Файл {SETTINGS_FILE} не найден.")
        return None
    
    with open(SETTINGS_FILE, "r") as file:
        try:
            settings = json.load(file)
            return settings
        except json.JSONDecodeError:
            print("Ошибка: неверный формат settings.json")
            return None

async def resolve_groups(client, groups):
    """
    Преобразование ссылок групп в ID, если это необходимо.
    """
    resolved_ids = []
    for group in groups:
        if isinstance(group, int):  # Если это уже ID
            resolved_ids.append(group)
        elif isinstance(group, str):  # Если это ссылка
            try:
                entity = await client.get_entity(group)
                resolved_ids.append(entity.id)
            except Exception as e:
                print(f"Ошибка при обработке группы {group}: {e}")
    return resolved_ids

async def start_client(session_path, api_id, api_hash, settings):
    """
    Запуск клиента и настройка событий.
    """
    print(f"Запуск сессии {session_path}...")
    client = TelegramClient(session_path, api_id, api_hash)

    await client.connect()
    if not (await client.is_user_authorized()):
        print('Аккаунт разлогинен.')
        await client.disconnect()
        return None

    groups = settings.get("groups", [])
    resolved_groups = await resolve_groups(client, groups)
    print(resolved_groups)
    reactions = settings["reactions"]
    emojis = reactions["emojis"]
    random_emojis = reactions.get("random_emojis", True)
    send_delay = reactions.get("send_delay", 200) / 1000
    ignore_messages = set(reactions.get("ingore_messages", []))
    last_messages_count = reactions.get("last_messages_count", 0)
    admin_bypass = reactions.get("admin_bypass", False)

    work_intervals = reactions.get("work_intervals", {"active_minutes": 10, "pause_minutes": 20})
    active_time = work_intervals["active_minutes"] * 60
    pause_time = work_intervals["pause_minutes"] * 60

    active = True

    @client.on(events.NewMessage(chats=resolved_groups))
    async def handler(event):
        """
        Обработчик новых сообщений в группах.
        """
        if not event.is_group or not active:
            return

        if event.id in ignore_messages:
            print(f"Сообщение {event.id} проигнорировано (в списке исключений).")
            return

        if admin_bypass and (await event.get_sender()).participant.admin_rights:
            print(f"Сообщение {event.id} проигнорировано (администратор).")
            return

        if last_messages_count > 0:
            messages = await client.get_messages(event.chat_id, limit=last_messages_count)
            if event.id not in [msg.id for msg in messages]:
                print(f"Сообщение {event.id} проигнорировано (вне последних {last_messages_count} сообщений).")
                return

        reaction = choice(emojis) if random_emojis else emojis[0]
        try:
            await client(SendReactionRequest(
                peer=event.chat_id,
                msg_id=event.id,
                reaction=[reaction]
            ))
            print(f"Поставлена реакция {reaction} на сообщение {event.id} в группе {event.chat_id}")
        except ChatAdminRequiredError:
            print(f"Недостаточно прав для реакции в группе {event.chat_id}")
        except Exception as e:
            print(f"Ошибка при установке реакции: {e}")

        await asyncio.sleep(send_delay)

    async def work_cycle():
        """
        Циклическое управление активностью клиента.
        """
        nonlocal active
        while True:
            print(f"Активная фаза {active_time // 60} минут.")
            active = True
            await asyncio.sleep(active_time)

            print(f"Пауза {pause_time // 60} минут.")
            active = False
            await asyncio.sleep(pause_time)

    asyncio.create_task(work_cycle())

    print(f"Сессия {session_path} запущена и подключена.")
    return client

async def main():
    """
    Основной цикл запуска сессий.
    """
    if not os.getenv("API_ID") or not os.getenv("API_HASH"):
        print("API_ID и API_HASH должны быть указаны в переменных окружения.")
        return

    api_id = int(os.getenv("API_ID"))
    api_hash = os.getenv("API_HASH")
    settings = await load_settings()
    if not settings:
        print("Настройки не загружены.")
        return

    session_files = [
        os.path.join(SESSION_FOLDER, f) 
        for f in os.listdir(SESSION_FOLDER) 
        if f.endswith(".session")
    ]

    if not session_files:
        print("Сессии не найдены в папке sessions.")
        return

    clients = []
    for session_file in session_files:
        client = await start_client(session_file, api_id, api_hash, settings)
        if not client:
            continue
        clients.append(client)

    try:
        await asyncio.gather(*[client.run_until_disconnected() for client in clients])
    except KeyboardInterrupt:
        print("Остановка всех сессий...")
        for client in clients:
            await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
