# main_final.py
import os
import sys

# ПРИНУДИТЕЛЬНО отключаем aiodns ДО импорта aiohttp
os.environ['AIOHTTP_NO_EXTENSIONS'] = '1'

import asyncio
import colorama
import aiohttp
import socket

# Для Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

from tgbot.services.sqlite import create_db
from tgbot.utils.other_functions import update_profit_week, update_profit_day, autobackup_db
from tgbot.handlers import setup_handlers
from tgbot.middlewares import setup_middlewares
from tgbot.data.config import bot_token
from apscheduler.schedulers.asyncio import AsyncIOScheduler

colorama.init()

async def main():
    # Создаем базу данных
    create_db()
    
    # Создаем connector с IPv4
    connector = aiohttp.TCPConnector(family=socket.AF_INET)
    
    # Создаем aiohttp сессию с нашим connector
    http_session = aiohttp.ClientSession(connector=connector)
    
    # Создаем aiogram сессию с нашей aiohttp сессией
    session = AiohttpSession()
    session._session = http_session  # Присваиваем нашу сессию
    
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
        # Закрываем сессию
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())