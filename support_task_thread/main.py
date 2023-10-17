import logging
import sys
from aiohttp import web
from aiogram import Router
from aiogram import Bot
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from core.db import database
from core.handlers.user.support import user_support_router, command_support_router
from core.handlers.admin.support import admin_support_router
from core.config.config import bot, dp, app, webhook_url, webhook_path, server_port
from core.middleware.middleware import AdminMiddleware

# from aiogram.utils.callback_answer import CallbackAnswerMiddleware
# Все обработчики должны быть прикреплены к Маршрутизатору - Router (или Диспетчеру)
routers = Router()
routers.include_routers(command_support_router, user_support_router, admin_support_router)


async def on_startup(bot: Bot) -> None:
    # Если у вас есть самоподписанный сертификат SSL, вам нужно будет отправить публичный
    # сертификат в Telegram
    await bot.set_webhook(f"{webhook_url}{webhook_path}")



def main() -> None:
    # подключение к базе данных
    database.DataBase().create()
    # Добавляет команды в кнопке

    # ... и все остальные роутеры должны быть подключены к Dispatcher
    dp.include_routers(routers)
    # Зарегистрируйте перехватчик запуска для инициализации веб-перехватчика
    dp.startup.register(on_startup)

    # Создается экземпляр обработчика запроса,
    # aiogram имеет несколько реализаций для разных случаев использования
    # В этом примере мы используем SimpleRequestHandler, который предназначен для обработки простых случаев.
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )

    dp.message.middleware.register(AdminMiddleware())

    # Регистрация обработчика веб-перехватчика в приложении
    webhook_requests_handler.register(app, path=webhook_path)

    # Подключение диспетчера запуск и завершения работы приложения aiohttp.
    setup_application(app, dp, bot=bot)

    # запускаем веб-сервер
    # web.run_app(app, host=config.server_host, port=config.server_port)
    web.run_app(app, port=server_port)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
