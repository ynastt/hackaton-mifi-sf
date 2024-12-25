import asyncio
import logging
# from dotenv import load_dotenv
# import os

from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_reader import config

logging.basicConfig(level=logging.INFO)

# load_dotenv() 
# TOKEN = os.getenv('TGBOT_TOKEN')
TOKEN = config.tgbot_token.get_secret_value()

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.reply("Привет!👋\nЯ твой помощник-гид по музейным экспонатам!\n\nПришли мне фото экспоната, о котором хочешь узнать подробнее📷")

@dp.message(F.photo)
async def command_download_photo(message: types.Message, bot: Bot):
    # await bot.download(
    #     message.photo[-1],
    #     destination=f"/photo/{message.photo[-1].file_id}.jpg"
    # )
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await message.bot.get_file(file_id)

    file_path = file.file_path
    download_path = "photo/photo.jpg"
    await bot.download_file(file_path, download_path)

    await message.answer("Ваша фотография принята в обработку")
    # TODO: сделать ответ с результатом от модели и 
    # добавить кнопки для дальнейших действий

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Оставить комментарий",
        callback_data="add_comment")
    )
    builder.add(types.InlineKeyboardButton(
        text="Загрузить новое фото",
        callback_data="add_photo")
    )
    builder.add(types.InlineKeyboardButton(
        text="Посмотреть комментарии",
        callback_data="get_comments")
    )
    builder.adjust(1)

    await message.answer(
        "Нажмите на кнопку для выбора дальнейшего действия",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "add_comment")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Напишите комментарий!")
    await callback.answer()

@dp.callback_query(F.data == "add_photo")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Отправьте новый снимок!")
    await callback.answer()

@dp.callback_query(F.data == "get_comments")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Спсиок комментариев:")
    # TODO: добавить вставку списка комментариев по экспонату из базы данных
    await callback.answer()

@dp.message(F.text)
async def cmd_start(message: types.Message):
    # TODO: добавить обработку комментария в модели, определяющей тональность текста
    await message.answer("Ответ модели с тональностью текста комментария")

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())