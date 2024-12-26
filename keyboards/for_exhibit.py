from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Клавиатура с инлайн кнопками
def get_comment_and_photo_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Оставить комментарий",
        callback_data="add_comment")
    )
    builder.add(InlineKeyboardButton(
        text="Загрузить новое фото",
        callback_data="add_photo")
    )
    builder.add(InlineKeyboardButton(
        text="Посмотреть комментарии",
        callback_data="get_comments")
    )
    builder.adjust(1)
    return builder.as_markup()