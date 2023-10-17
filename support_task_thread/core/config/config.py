from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiohttp import web

"""
используется веб-перехватчик позади любого обратного прокси-сервера (nginx, traefik, ingress etc.).
я использую ngrok для тестов.
"""

"""
                                            Настройки сервера.
                                            
- token_api: можно получить здесь: https://t.me/BotFather.
- server_host: Привязывайте локальный хост только для предотвращения внешнего доступа.
- server_port: Порт для входящего запроса от обратного прокси. Должен быть любой доступный порт.
- webhook_url: Путь к маршруту веб-хука, по которому Telegram будет отправлять запросы.
- webhook_path: часть пути, на который мы будем принимать запросы.
- support_chat_id: группа, в которую будут отправлять запросы от пользователей.
"""

token_api = "6106569568:AAtEF-jrIg5R8bc3vSsOfM1voY8mWrQgVTY"
server_host = "127.0.0.1"
server_port = "80"
webhook_url = "https://748-8578-235-1e53-.ngrok-free.app"
webhook_path = "/AAc9zj95Iz3jQ6ejEHjx_b2No6LgKijFq"
support_chat_id = "-0181989700946"
os = "windows"


def path_db():
    if os == "linux":
        return "data/db.db"
    elif os == "windows":
        return "data\\db.db"


# Создайте экземпляр aiohttp.web.Application.
app = web.Application()
# Инициализируйте экземпляр бота с режимом анализа по умолчанию, который будет передаваться всем вызовам API.
bot = Bot(token_api, parse_mode=ParseMode.HTML)

# Диспетчер — корневой маршрутизатор
dp = Dispatcher()


async def check_admin_group(user_id):
    chat_admins = await bot.get_chat_administrators(support_chat_id)
    for admins in chat_admins:
        if user_id == admins.user.id and user_id != bot.id:
            return True
    return False
