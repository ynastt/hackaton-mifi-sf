from aiogram import Router, F, types, Bot
from aiogram.filters import CommandStart

from keyboards.for_exhibit import get_comment_and_photo_kb

router = Router() 

# Хэндлер на команду /start
@router.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.reply("Привет!👋\nЯ твой помощник-гид по музейным экспонатам!\n\nПришли мне фото экспоната, о котором хочешь узнать подробнее📷")

# Хэндлер на команду отправленной фотографии
@router.message(F.photo)
async def command_download_photo(message: types.Message, bot: Bot):
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await message.bot.get_file(file_id)

    file_path = file.file_path
    download_path = "photo/photo.jpg"
    await bot.download_file(file_path, download_path)

    await message.answer("Ваша фотография принята в обработку")
    # TODO: сделать ответ с результатом от модели

    await message.answer(
        "Нажмите на кнопку для выбора дальнейшего действия",
        reply_markup=get_comment_and_photo_kb()
    )

# Хэндлер на кнопку "Оставить комментарий"
@router.callback_query(F.data == "add_comment")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Напишите комментарий!")
    await callback.answer()

# Хэндлер на кнопку "Загрузить новое фото"
@router.callback_query(F.data == "add_photo")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Отправьте новый снимок!")
    await callback.answer()

# Хэндлер на кнопку "Посмотреть комментарии"
@router.callback_query(F.data == "get_comments")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Спсиок комментариев:")
    # TODO: добавить вставку списка комментариев по экспонату из базы данных
    await callback.answer()

# Хэндлер на текстовое сообщения комментария пользователя
@router.message(F.text)
async def cmd_start(message: types.Message):
    # TODO: сохранить комментарий в базу
    # TODO: добавить обработку комментария в модели, определяющей тональность текста
    await message.answer("Ответ модели с тональностью текста комментария")