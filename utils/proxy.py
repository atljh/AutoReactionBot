from .settings import load_settings, save_settings

def add_proxy(proxy: str):
    settings = load_settings()
    proxies = settings.get('proxy', [])
    proxies.append(proxy)
    settings['proxy'] = proxies
    save_settings(settings)

def delete_proxy(proxy: str):
    settings = load_settings()
    proxies = settings.get('proxy', [])
    proxies.remove(proxy)
    settings['proxy'] = proxies
    save_settings(settings)