# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.data.config import bot_token

# Создаем сессию без connector при инициализации
# Connector будет создан автоматически при необходимости
session = AiohttpSession()

# Создаем бота с нашей сессией
bot = Bot(
    token=bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=session
)

# Создаем диспетчер с хранилищем
dp = Dispatcher(storage=MemoryStorage())

# Планировщик задач
scheduler = AsyncIOScheduler()