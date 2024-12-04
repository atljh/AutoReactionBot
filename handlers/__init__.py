from aiogram import Router

from .main_menu import router as start_router
from .account import router as account_router
from .group import router as group_router
from .settings import router as settings_router
from .userbot import router as userbot_router

router = Router(name=__name__)
router.include_router(start_router)
router.include_router(account_router)
router.include_router(group_router)
router.include_router(settings_router)
router.include_router(userbot_router)

__all__ = ("router",)
