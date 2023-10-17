import asyncio
import logging
import sys
from aiogram.filters import Command
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.markdown import hbold



# Токен бота можно получить здесь: https://t.me/BotFather
TOKEN = " "

# Все обработчики должны быть прикреплены к Маршрутизатору (или Диспетчеру)
dp = Dispatcher()


@dp.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


async def main() -> None:
    # Инициализируем экземпляр бота с режимом анализа по умолчанию, который будет передаваться всем вызовам API.
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # И диспетчеризация событий запуска
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
