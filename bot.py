import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_reader import config
from handlers import commands

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Получение токена из конфига
TOKEN = config.tgbot_token.get_secret_value()

async def main():
    # Объект бота
    bot = Bot(token=TOKEN)
    # Диспетчер
    dp = Dispatcher()

    # Регистрируем роутеры из других файлов
    dp.include_routers(commands.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())