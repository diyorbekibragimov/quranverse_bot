from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_data import language, chapter_data, pagination

language_choice = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text="\U0001F1FA\U0001F1F8 English", callback_data=language.new(
                code="en"
            )),
            InlineKeyboardButton(text="\U0001F1F7\U0001F1FA Русский", callback_data=language.new(
                code="ru"
            ))
        ]
    ]
)

def generate_chapter_kb(first_chapter, last_chapter):
    chapter_kb = InlineKeyboardMarkup()
    for i in range(first_chapter, last_chapter+1):
        btn = InlineKeyboardButton(text=str(i), callback_data=chapter_data.new(
            chapter_id=i
        ))
        chapter_kb.insert(btn)

    btn_back = InlineKeyboardButton(text="\U00002B05\U0000FE0F", callback_data=pagination.new(
        key="back"
    ))
    btn_forward = InlineKeyboardButton(text="\U000027A1\U0000FE0F", callback_data=pagination.new(
        key="forward"
    ))
    chapter_kb.row(btn_back, btn_forward)
    return chapter_kb

verses_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text="\U00002B05\U0000FE0F", callback_data=pagination.new(
                key="back_verse"
            )),
            InlineKeyboardButton(text="\U000027A1\U0000FE0F", callback_data=pagination.new(
                key="forward_verse"
            ))
        ]
    ]
)