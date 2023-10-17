"""
This example shows how to use webhook on behind of any reverse proxy (nginx, traefik, ingress etc.)
"""
import asyncio
import logging
import sys
import json
from aiohttp import web
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.utils.markdown import hbold

"""
используется веб-перехватчик позади любого обратного прокси-сервера (nginx, traefik, ingress etc.).
я использую ngrok для тестов.
"""

"""
                                            Настройки сервера.
Привязывайте локальный хост только для предотвращения внешнего доступа:
- token_api: можно получить здесь: https://t.me/BotFather.
- server_host.
- server_port: Порт для входящего запроса от обратного прокси. Должен быть любой доступный порт.
- webhook_url: Путь к маршруту веб-хука, по которому Telegram будет отправлять запросы.
- webhook_path: часть пути, на который мы будем принимать запросы.
"""

token_api = "6681065695:AAEtF-jrIbc3vg5R8oY8mMSsOfv1WrQgVTY"
server_host = "127.0.0.1"
server_port = "80"
webhook_url = "https://7e48-85-235-53-178.ngrok-free.app"
webhook_path = "/AAEH6e3jQjx_b2zNjjc9zj95Ioi6LgKFq"
support_chat_id = "-1001980897946"
os = "windows"

# Все обработчики должны быть прикреплены к Маршрутизатору (или Диспетчеру)
router = Router()


@router.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


async def on_startup(bot: Bot) -> None:
    # Если у вас есть самоподписанный сертификат SSL, вам нужно будет отправить публичный
    # сертификат в Telegram
    await bot.set_webhook(f"{webhook_url}{webhook_path}")


def main() -> None:


    # Диспетчер — корневой маршрутизатор
    dp = Dispatcher()
    # ... и все остальные роутеры должны быть подключены к Dispatcher
    dp.include_router(router)

    # Зарегистрируйте перехватчик запуска для инициализации веб-перехватчика
    dp.startup.register(on_startup)

    # Инициализируйте экземпляр бота с режимом анализа по умолчанию, который будет передаваться всем вызовам API.
    bot = Bot(token_api, parse_mode=ParseMode.HTML)

    # Создайте экземпляр aiohttp.web.Application.
    app = web.Application()

    # Создается экземпляр обработчика запроса,
    # aiogram имеет несколько реализаций для разных случаев использования
    # В этом примере мы используем SimpleRequestHandler, который предназначен для обработки простых случаев.
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    # Регистрация обработчика веб-перехватчика в приложении
    webhook_requests_handler.register(app, path=webhook_path)

    # Подключение диспетчера запуск и завершения работы приложения aiohttp.
    setup_application(app, dp, bot=bot)

    # запускаем веб-сервер
    web.run_app(app, port=server_port)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
