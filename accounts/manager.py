from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from pathlib import Path
import json

ACCOUNTS_FILE = Path("accounts.json")

async def load_accounts():
    if ACCOUNTS_FILE.exists():
        with open(ACCOUNTS_FILE, "r") as f:
            return json.load(f)
    return []

async def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f)

async def add_account(phone, api_id, api_hash):
    client = TelegramClient(f"sessions/{phone}", api_id, api_hash)
    await client.start(phone=phone)
    accounts = await load_accounts()
    accounts.append({"phone": phone, "api_id": api_id, "api_hash": api_hash})
    await save_accounts(accounts)

async def list_accounts():
    return await load_accounts()

async def delete_account(account_id):
    accounts = await load_accounts()
    accounts = [a for a in accounts if a.get("id") != account_id]
    await save_accounts(accounts)
