from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from core.config.config import check_admin_group


def set_access_key(key: str = None):
    def decorator(func):
        setattr(func, 'key', key)
        return func
    return decorator


class AdminMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        key = get_flag(data, "key")
        if key == 'admin' and await check_admin_group(event.from_user.id):
            return await handler(event, data)
        elif key == 'user':
            return await handler(event, data)
