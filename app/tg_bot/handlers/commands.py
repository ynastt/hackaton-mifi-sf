import base64
import json
import re
from io import BytesIO
from uuid import UUID

import aio_pika
from aiogram import Router, F, types, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from app.armq.connection import channel_pool
from app.tg_bot.keyboards.for_exhibit import get_comment_and_photo_kb
from app.tg_bot.states.get_data_states import GetDataState
from app.config_reader import config
from app.database.cruds import DatabaseCRUDS

router = Router()


# Хэндлер на команду /start
@router.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.reply(
        "Привет!👋\nЯ твой помощник-гид по музейным экспонатам!\n\nПришли мне фото экспоната, о котором хочешь узнать подробнее📷")


# Хэндлер на команду отправленной фотографии
@router.message(F.photo)
async def command_download_photo(message: types.Message, bot: Bot, db: DatabaseCRUDS, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await message.bot.get_file(file_id)

    file_path = file.file_path
    photo_bytes_io = BytesIO()
    await bot.download_file(file_path, photo_bytes_io)
    photo_bytes_io.seek(0)
    photo_base64 = base64.b64encode(photo_bytes_io.read()).decode("utf-8")
    async with channel_pool.acquire() as channel:
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps({'photo': photo_base64,
                                 'tg_id': message.from_user.id}).encode('utf-8')
            ),
            routing_key=config.CV_QUEUE_NAME,
        )
    await message.answer("Ваша фотография принята в обработку")


# Хэндлер на кнопку "Оставить комментарий"
@router.callback_query(lambda callback: re.search(r'add_comment_', callback.data))
async def send_random_value(callback: types.CallbackQuery, db: DatabaseCRUDS, state: FSMContext):
    await callback.message.answer("Напишите комментарий!")
    await state.set_state(GetDataState.add_comment)
    exhibit_id = UUID(callback.data.split('_')[-1])
    await state.update_data(exhibit_id=str(exhibit_id))


# Хэндлер на кнопку "Загрузить новое фото"
@router.callback_query(F.data == "add_photo")
async def send_random_value(callback: types.CallbackQuery, db: DatabaseCRUDS, state: FSMContext):
    await callback.message.answer("Отправьте новый снимок!")
    await callback.answer()


# Хэндлер на кнопку "Посмотреть комментарии"
@router.callback_query(lambda callback: re.search(r"get_comments_", callback.data))
async def send_random_value(callback: types.CallbackQuery, db: DatabaseCRUDS, state: FSMContext):
    await callback.message.answer("Спсиок комментариев:")
    exhibit_id = UUID(callback.data.split('_')[-1])
    comments = await db.get_comments_by_exhibit_id(exhibit_id)
    sent_mapping = {
        0: "Негативный комментарий",
        1: "Нейтральный комментарий",
        2: "Положительный комментарий",
    }
    comments_string = '\n\n\n'.join([comment.comment + '\n' + sent_mapping[comment.sentiment] for comment in comments])
    await callback.message.answer(comments_string, reply_markup=get_comment_and_photo_kb(exhibit_id))


# Хэндлер на текстовое сообщения комментария пользователя
@router.message(GetDataState.add_comment, F.text)
async def cmd_start(message: types.Message, db: DatabaseCRUDS, state: FSMContext):
    data = await state.get_data()
    comment = await db.add_comment(message.text, UUID(data.get('exhibit_id')))
    async with channel_pool.acquire() as channel:
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps({'message': message.text,
                                 'exhibit_id': data.get('exhibit_id'),
                                 'tg_id': message.from_user.id,
                                 'comment_id': str(comment.id)}).encode('utf-8')
            ),
            routing_key=config.NLP_QUEUE_NAME,
        )
    await message.answer("Пожалуйста, подождите...")
    await state.clear()
