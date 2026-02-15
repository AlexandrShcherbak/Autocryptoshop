# start_bot.py
import os
import sys

# УДАЛЯЕМ aiodns из sys.path до импорта aiohttp
for path in list(sys.path):
    if 'aiodns' in path or 'pycares' in path:
        sys.path.remove(path)

# Отключаем расширения
os.environ['AIOHTTP_NO_EXTENSIONS'] = '1'

# Монки-патч модуля resolver ДО импорта aiohttp
import aiohttp.resolver

# Создаем синхронный резолвер
class SyncResolver:
    def __init__(self, *args, **kwargs):
        pass
    
    async def resolve(self, host, port=0, family=0):
        import socket
        # Синхронный DNS
        infos = socket.getaddrinfo(
            host=host,
            port=port,
            family=family or socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
            flags=socket.AI_ADDRCONFIG
        )
        return [info[4][0] for info in infos]

# Заменяем AsyncResolver в aiohttp.resolver
aiohttp.resolver.AsyncResolver = SyncResolver

# Теперь импортируем aiohttp
import aiohttp

# Также патчим connector
original_create_connector = aiohttp.TCPConnector.__init__

def patched_connector_init(self, *args, **kwargs):
    # Убираем resolver из kwargs
    kwargs.pop('resolver', None)
    # Используем наш резолвер
    kwargs['resolver'] = SyncResolver()
    # Форсируем IPv4
    kwargs['family'] = socket.AF_INET
    return original_create_connector(self, *args, **kwargs)

aiohttp.TCPConnector.__init__ = patched_connector_init

import asyncio
import socket
import colorama

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

from tgbot.services.sqlite import create_db
from tgbot.utils.other_functions import update_profit_week, update_profit_day, autobackup_db
from tgbot.services.http_client import close_shared_sessions
from tgbot.handlers import setup_handlers
from tgbot.middlewares import setup_middlewares
from tgbot.data.config import bot_token
from apscheduler.schedulers.asyncio import AsyncIOScheduler

colorama.init()

async def main():
    # Создаем базу данных
    create_db()
    
    # Создаем connector с нашим патчем
    connector = aiohttp.TCPConnector()
    
    # Создаем сессию
    session = AiohttpSession()
    
    # Патчим внутреннюю сессию aiohttp
    session._session = aiohttp.ClientSession(connector=connector)
    
    # Создаем бота
    bot = Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode="HTML"),
        session=session
    )
    
    # Создаем диспетчер
    dp = Dispatcher(storage=MemoryStorage())
    
    # Настраиваем мидлвары
    setup_middlewares(dp)
    
    # Регистрируем обработчики
    setup_handlers(dp)
    
    # Планировщик
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_profit_week, "cron", day_of_week="mon", hour=0)
    scheduler.add_job(update_profit_day, "cron", hour=0)
    scheduler.add_job(autobackup_db, "cron", hour=0)
    scheduler.start()
    
    print(colorama.Fore.GREEN + "=======================")
    print(colorama.Fore.RED + "Bot Was Started")
    print(colorama.Fore.RESET)
    
    try:
        # Запускаем поллинг
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await close_shared_sessions()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
