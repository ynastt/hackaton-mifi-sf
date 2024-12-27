from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Клавиатура с инлайн кнопками
def get_comment_and_photo_kb(exhibit_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Оставить комментарий",
        callback_data=f"add_comment_{exhibit_id}")
    )
    builder.add(InlineKeyboardButton(
        text="Загрузить новое фото",
        callback_data="add_photo")
    )
    builder.add(InlineKeyboardButton(
        text="Посмотреть комментарии",
        callback_data=f"get_comments_{exhibit_id}")
    )
    builder.adjust(1)
    return builder.as_markup()