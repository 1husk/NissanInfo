from aiogram import Bot,types
from aiogram.dispatcher import Dispatcher
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = '<token>'
APP_NAME = '<app_name>'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)