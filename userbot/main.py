import os
import asyncio
from random import choice, randint

from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.errors.rpcerrorlist import ChatAdminRequiredError, UserNotParticipantError
from telethon.tl.types import ReactionEmoji

from utils.settings import load_settings, save_settings
from utils.proxy import get_proxy, delete_proxy
from utils.console import console
from utils.config import load_config

config = load_config()

SESSION_FOLDER = "sessions"
os.makedirs(SESSION_FOLDER, exist_ok=True)


async def resolve_groups(client, groups):
    """
    Преобразование ссылок групп в ID, если это необходимо.
    """
    resolved_ids = []
    for group in groups:
        if isinstance(group, int):
            resolved_ids.append(group)
        elif isinstance(group, str):
            try:
                entity = await client.get_entity(group)
                resolved_ids.append(entity.id)
            except Exception as e:
                console.log(f"Ошибка при обработке группы {group}: {e}")
    return resolved_ids


async def react_to_last_messages(client, chat_id, settings, active):
    """
    Пройтись по последним сообщениям группы и добавить реакции.
    """
    if not active:
        return

    reactions = settings["reactions"]
    emojis = reactions["emojis"]
    random_emojis = reactions.get("random_emojis", True)
    send_delay = reactions.get("send_delay", 10)
    ignore_messages_range = reactions.get("ignore_messages", [1, 3])
    last_messages_count = reactions.get("last_messages_count", 0)

    try:
        messages = await client.get_messages(chat_id, limit=last_messages_count)
        console.log(f"Обрабатывается {len(messages)} сообщений в группе {chat_id}")

        for i, message in enumerate(messages):
            if i % randint(*ignore_messages_range) == 0:
                console.log(f"Сообщение {message.id} проигнорировано.")
                continue

            reaction = choice(emojis) if random_emojis else emojis[0]
            try:
                await client(SendReactionRequest(
                    peer=chat_id,
                    msg_id=message.id,
                    reaction=[ReactionEmoji(emoticon=reaction)]
                ))
                console.log(f"Реакция {reaction} добавлена к сообщению {message.id}.")
            except ChatAdminRequiredError:
                console.log(f"Недостаточно прав для реакции в группе {chat_id}.")
                return
            except Exception as e:
                console.log(f"Ошибка при установке реакции: {e}")
                if "Invalid reaction" in str(e):
                    console.log(f"Удаляем некорректную реакцию: {reaction}")
                    emojis.remove(reaction)
                    save_settings(settings)
                    if not emojis:
                        console.log("Больше нет доступных эмодзи для отправки.")
                        return

            await asyncio.sleep(send_delay)

    except Exception as e:
        console.log(f"Ошибка при обработке сообщений группы {chat_id}: {e}")


async def start_client(session_path, api_id, api_hash, settings):
    """
    Запуск клиента и настройка событий.
    """
    proxy = get_proxy()
    if proxy:
        try:
            client = TelegramClient(session_path, api_id, api_hash, proxy=proxy[0])
            await client.connect()
        except TypeError:
            console.log("Неправильный формат прокси")
            delete_proxy(proxy)
    else:
        client = TelegramClient(session_path, api_id, api_hash)
        await client.connect()

    if not (await client.is_user_authorized()):
        console.log(f'Аккаунт {session_path[9:]} разлогинен.')
        await client.disconnect()
        return None

    groups = settings.get("groups", [])
    resolved_groups = await resolve_groups(client, groups)
    reactions = settings["reactions"]
    emojis = reactions["emojis"]
    random_emojis = reactions.get("random_emojis", True)
    send_delay = reactions.get("send_delay", 10)
    ignore_messages_range = reactions.get("ignore_messages", [1, 3])
    last_messages_count = reactions.get('last_messages_count', 0)

    work_intervals = reactions.get("work_intervals", {"active_minutes": 10, "pause_minutes": 20})
    active_time = work_intervals["active_minutes"] * 60
    pause_time = work_intervals["pause_minutes"] * 60

    active = True

    async def work_cycle():
        """
        Циклическое управление активностью клиента.
        """
        nonlocal active
        while True:
            console.log(f"Активная фаза {active_time // 60} минут.")
            active = True
            await asyncio.sleep(active_time)

            console.log(f"Пауза {pause_time // 60} минут.")
            active = False
            await asyncio.sleep(pause_time)

    asyncio.create_task(work_cycle())

    if last_messages_count > 0:
        for group_id in resolved_groups:
            await react_to_last_messages(client, group_id, settings, active)
            
    @client.on(events.NewMessage(chats=resolved_groups))
    async def handler(event):
        """
        Обработчик новых сообщений в группах.
        """
        if not event.is_group or not active:
            return

        if event.id % randint(*ignore_messages_range) == 0:
            console.log(f"Сообщение {event.id} проигнорировано (в диапазоне ignore_messages).")
            return
        
        settings = load_settings()
        reactions = settings["reactions"]
        admin_bypass = reactions.get("admin_bypass", False)

        try:
            sender = await event.get_sender()            
            permissions = await client.get_permissions(event.chat_id, sender)

            if admin_bypass and permissions.is_admin:
                console.log(f"Сообщение проигнорировано (администратор).")
                return
            
        except UserNotParticipantError:
            console.log(f"Пользователь не является участником группы.")
        except Exception as e:
            console.log(f"Ошибка при получении участника: {e}")
            return

        reaction = choice(emojis) if random_emojis else emojis[0]
        try:
            await client(SendReactionRequest(
                peer=event.chat_id,
                msg_id=event.id,
                reaction=[ReactionEmoji(emoticon=reaction)]
            ))
            console.log(f"Поставлена реакция {reaction} в группе {event.chat_id}")
        except ChatAdminRequiredError:
            console.log(f"Недостаточно прав для реакции в группе {event.chat_id}")
        except Exception as e:
            console.log(f"Ошибка при установке реакции: {e}")
            if "Invalid reaction" in str(e):
                console.log(f"Удаляем некорректную реакцию: {reaction}")
                emojis.remove(reaction)
                save_settings(settings)
                if not emojis:
                    console.log("Больше нет доступных эмодзи для отправки.")
                    return
        await asyncio.sleep(send_delay)

    console.log(f"Сессия {session_path[9:]} запущена.")
    return client


async def main():
    """
    Основной цикл запуска сессий.
    """
    if not config.get("api_hash") or not config.get("api_id"):
        console.log("api_id и api_hash должны быть указаны в переменных окружения.")
        return

    api_id = int(config.get("api_id"))
    api_hash = config.get("api_hash")
    settings = load_settings()
    if not settings:
        console.log("Настройки не загружены.")
        return

    session_files = [
        os.path.join(SESSION_FOLDER, f)
        for f in os.listdir(SESSION_FOLDER)
        if f.endswith(".session")
    ]

    if not session_files:
        console.log("Сессии не найдены в папке sessions.")
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
        console.log("Остановка всех сессий...")
        for client in clients:
            await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
