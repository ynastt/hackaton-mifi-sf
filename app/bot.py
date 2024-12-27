import asyncio
from app.logs.logs import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from app.tg_bot.middlewares.db import DatabaseMiddleware
from app.database.connection import session
from app.config_reader import config
from app.tg_bot.handlers import commands

# Получение токена из конфига
TOKEN = config.BOT_TOKEN.get_secret_value()


async def main():
    # Объект бота
    bot = Bot(token=TOKEN)
    # Диспетчер
    dp = Dispatcher()
    dp.update.middleware(DatabaseMiddleware(session=session))

    # Регистрируем роутеры из других файлов
    dp.include_routers(commands.router)
    user_commands = [
        BotCommand(command="start", description="Старт / главное меню")
    ]
    await bot.set_my_commands(user_commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
