import json
import os

from .emojis import filter_valid_emojis

SETTINGS_FILE = "settings.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        print(f"Файл {SETTINGS_FILE} не найден.")
        create_default_settings()
        return None

    with open(SETTINGS_FILE, "r") as file:
        try:
            settings = json.load(file)
        except json.JSONDecodeError:
            print("Ошибка: неверный формат settings.json")
            return None

    if "reactions" in settings and "emojis" in settings["reactions"]:
        emojis = settings["reactions"]["emojis"]
        valid_emojis = filter_valid_emojis(emojis)

        if len(valid_emojis) < len(emojis):
            print("Найдены невалидные эмодзи. Они будут удалены из настроек.")
            settings["reactions"]["emojis"] = valid_emojis

            with open(SETTINGS_FILE, "w") as file:
                json.dump(settings, file, indent=4, ensure_ascii=False)

    return settings

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

def update_setting(key, value):
    settings = load_settings()
    keys = key.split(".")
    temp = settings

    for k in keys[:-1]:
        temp = temp.setdefault(k, {})

    temp[keys[-1]] = value
    save_settings(settings)
    print(f"Настройка {key} обновлена на {value}")

def create_default_settings():
    default_settings = {
        "reactions": {
            "emojis": ["👍", "😁", "🥰"],
            "send_delay": 5,
            "random_emojis": True,
            "ingore_messages": [1, 5],
            "work_intervals": {
                "active_minutes": 12,
                "pause_minutes": 30
            },
            "admin_bypass": True,
            "last_messages_count": 10
        },
        "groups": {
        },
        "proxy": [
        ],
        "active_groups": [
        ]
    }
    save_settings(default_settings)

settings = load_settings()
