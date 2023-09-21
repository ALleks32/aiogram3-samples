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

# заполни empty_setting
# переименуй empty_setting -> setting
with open('setting.json', 'r') as data:
    json_data = json.load(data)

# Токен бота можно получить здесь: https://t.me/BotFather
TOKEN = str(json_data['token_api'])

# Настройки сервера
# привязывайте локальный хост только для предотвращения внешнего доступа
WEB_SERVER_HOST = str(json_data['server_host'])
# Порт для входящего запроса от обратного прокси. Должен быть любой доступный порт
WEB_SERVER_PORT = int(json_data['server_port'])
# Путь к маршруту веб-хука, по которому Telegram будет отправлять запросы
WEBHOOK_PATH = '/' + str(json_data['webhook_path'])
# Базовый URL-адрес веб-перехватчика будет использоваться для создания URL-адреса веб-перехватчика для Telegram,
# Здесь используется публичный DNS с поддержкой HTTPS
BASE_WEBHOOK_URL = str(json_data['webhook_url'])

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
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")


def main() -> None:


    # Диспетчер — корневой маршрутизатор
    dp = Dispatcher()
    # ... и все остальные роутеры должны быть подключены к Dispatcher
    dp.include_router(router)

    # Зарегистрируйте перехватчик запуска для инициализации веб-перехватчика
    dp.startup.register(on_startup)

    # Инициализируйте экземпляр бота с режимом анализа по умолчанию, который будет передаваться всем вызовам API.
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

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
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    # Подключение диспетчера запуск и завершения работы приложения aiohttp.
    setup_application(app, dp, bot=bot)

    # запускаем веб-сервер
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
