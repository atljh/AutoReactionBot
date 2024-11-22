import json
import os

SETTINGS_FILE = "settings.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        create_default_settings()
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

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
            "emojis": ["👍", "❤️", "😂", "🔥"],
            "random_emojis": True,
            "ingore_messages": [1, 3],
            "work_intervals": {
                "active_minutes": 10,
                "pause_minutes": 20
            },
            "admin_bypass": True
        },
        "system": {
            "restart_command": "sudo systemctl restart bot",
            "log_level": "WARNING"
        }
    }
    save_settings(default_settings)

settings = load_settings()
