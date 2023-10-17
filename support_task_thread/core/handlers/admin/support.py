from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.config.config import bot
from core.db.support_db import SupportTicket

admin_key = {"key": "admin"}

admin_support_router = Router()


@admin_support_router.message(flags=admin_key)
async def get_dialog(message: Message, state: FSMContext):
    if message.message_thread_id:
        is_thread = SupportTicket().check_thread(message.message_thread_id)
        if is_thread:
            chat_id = SupportTicket().id_user(message.message_thread_id)
            await bot.copy_message(chat_id=chat_id,
                                   from_chat_id=message.chat.id,
                                   message_id=message.message_id)
