from .settings import load_settings, save_settings

def get_proxy():
    settings = load_settings()
    proxies = settings.get('proxy', [])
    return proxies if len(proxies) else None

def add_proxy(proxy: str):
    settings = load_settings()
    proxies = settings.get('proxy', [])
    proxies.append(proxy)
    settings['proxy'] = proxies
    save_settings(settings)

def delete_proxy(proxy: str):
    settings = load_settings()
    proxies = settings.get('proxy', [])
    if not proxy in proxies:
        return False
    proxies.remove(proxy)
    settings['proxy'] = proxies
    save_settings(settings)
    return True