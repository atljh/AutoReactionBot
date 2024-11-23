from .start import register_start_handlers
from .account import register_account_handlers
from .main_menu import register_main_menu_handlers
from .group import register_group_handlers
from .settings import register_settings_handlers
from .starter import register_starter_handlers

def setup_handlers(dp):
    register_start_handlers(dp)
    register_account_handlers(dp)
    register_main_menu_handlers(dp)
    register_group_handlers(dp)
    register_settings_handlers(dp)
    register_starter_handlers(dp)
