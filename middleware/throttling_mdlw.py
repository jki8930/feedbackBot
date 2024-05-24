from typing import Any, Callable, Dict, Awaitable

from aiogram.fsm.storage.redis import RedisStorage
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        message: Message,
        data: Dict[str, Any]
    ) -> Any:
        user = f"user{message.from_user.id}"
        check_user = await self.storage.redis.get_name(name=user)

        if check_user:
            if int(check_user.decode()) == 1:
                await self.storage.redis.set(name=user, value=0, ex=10)
                await message.answer("Замечена подозрительная активность, подождите 10 секунд.")
            return
        await self.storage.redis.set(name=user, value=1, ex=10)
        
        return await handler(message, data)
