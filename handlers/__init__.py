from aiogram import Router

from .user import router as user
from .admin import router as admin

router = Router()
router.include_routers(user, admin)