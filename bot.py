from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from filters import IsOwnerFilter, IsAdminFilter, MemberCanRestrictFilter
from keyboards.choice_buttons import language_choice, generate_chapter_kb, verses_kb
from keyboards.callback_data import language, chapter_data, pagination
from db import BotDB
from handle import get_verse, get_list_of_chapters, get_chapter, get_number_of_pages
import logging
import config

if not config.BOT_TOKEN:
    exit("No Token Provided")

# init
BotDB = BotDB("quran.db")
bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# activate filters
dp.filters_factory.bind(IsOwnerFilter)
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(MemberCanRestrictFilter)

class Language(StatesGroup):
    start = State()

class Chapter(StatesGroup):
    page_number = State()
    chapter_name = State()

class Verses(StatesGroup):
    page_number = State()
    chapter_id = State()

def instructions(language="en"):
    instruction = ""
    if language == "ru":
        instruction += "Привет друг! Просто введи ключ аята (1:1 - первый аят первой суры)"
    else:
        instruction += "Hi there! Just type a key of the verse (e.g. 1:1 - first verse of the first ayah)"
    return instruction

@dp.message_handler(state="*", commands="start")
async def start(message: Message):
    if (not BotDB.user_exists(message.from_user.id)):
        await message.bot.send_message(message.from_user.id, text="Choose your language (выберите язык):", reply_markup=language_choice)
    else:
        await Language.start.set()
        await message.bot.send_message(message.from_user.id, text="Choose your language (выберите язык):", reply_markup=language_choice)

@dp.callback_query_handler(chapter_data.filter(chapter_id=[str(x) for x in range(1, 115)]), state="*")
async def display_chapter(query: CallbackQuery, callback_data: dict, state: FSMContext):
    """ Display the verse that the user chose """
    chapter_number = callback_data["chapter_id"]
    language = BotDB.get_user_language(user_id=query.from_user.id)
    page_number = 1
    data = get_chapter(chapter_number, page_number, language)

    await Verses.page_number.set()
    await state.update_data(page_number=page_number, chapter_id=chapter_number)
    await query.message.answer(text=data, reply_markup=verses_kb)

@dp.callback_query_handler(pagination.filter(key=["back_verse", "forward_verse"]), state=Verses.page_number)
async def handle_verses_pagination(query: CallbackQuery, callback_data: dict, state: FSMContext):
    page_number = 0
    chapter_id = 0
    key = callback_data["key"]
    language = BotDB.get_user_language(user_id=query.from_user.id)

    async with state.proxy() as data:
        page_number = int(data["page_number"])
        chapter_id = int(data["chapter_id"])

    number_of_pages = int(get_number_of_pages(chapter_id))

    if key == "back_verse":
        page_number -= 1
    elif key == "forward_verse":
        page_number += 1

    if page_number != 0 and page_number != number_of_pages + 1:
        data = get_chapter(chapter_id, page_number, language)
        await state.update_data(page_number=page_number)
        await query.message.edit_text(text=data, reply_markup=verses_kb)
    else:
        return

@dp.callback_query_handler(pagination.filter(key=["back", "forward"]), state="*")
async def handle_pagination(query: CallbackQuery, callback_data: dict, state: FSMContext):
    page_number = 0
    key = callback_data["key"]
    language = BotDB.get_user_language(user_id=query.from_user.id)

    async with state.proxy() as data:
        page_number = int(data["page_number"])

    if key == "back":
        page_number -= 1
    elif key == "forward":
        page_number += 1

    if page_number != 0 and page_number != 9:
        response = get_list_of_chapters(page_number=page_number, language=language)
        start = 15 * (page_number - 1) + 1
        end = page_number*15
        if end == 120:
            end -= 6
        chapter_kb = generate_chapter_kb(start, end)

        await state.update_data(page_number=page_number)
        await query.message.edit_text(text=response, reply_markup=chapter_kb)
    else:
        return

@dp.message_handler(state="*", commands="chapter")
async def chapter(message: Message, state: FSMContext):
    page_number = 1
    language = BotDB.get_user_language(user_id=message.from_user.id)

    response = get_list_of_chapters(page_number=page_number, language=language)
    chapter_kb = generate_chapter_kb(page_number, page_number*15)

    await Chapter.page_number.set()
    await state.update_data(page_number=page_number)
    await message.bot.send_message(message.from_user.id, text=response, reply_markup=chapter_kb)

@dp.message_handler(state="*")
async def verse(message: Message, state: FSMContext):
    """Get the key from the input and display the verse"""
    key = message.text
    language = BotDB.get_user_language(user_id=message.from_user.id)
    response = get_verse(key, language)
    await message.bot.send_message(message.from_user.id, response)

@dp.callback_query_handler(language.filter(code='en'))
async def process_callback_language(query: CallbackQuery, callback_data: dict):
    await query.answer(cache_time=3)
    BotDB.add_user(user_id=query.from_user.id, language=callback_data["code"])
    await query.message.edit_text(text=instructions("en"))

@dp.callback_query_handler(language.filter(code='ru'))
async def process_callback_language(query: CallbackQuery, callback_data: dict):
    await query.answer(cache_time=3)
    BotDB.add_user(user_id=query.from_user.id, language=callback_data["code"])
    await query.message.edit_text(text=instructions("ru"))

@dp.callback_query_handler(language.filter(code='en'), state=Language.start)
async def process_callback_language(query: CallbackQuery, callback_data: dict):
    await query.answer(cache_time=3)
    BotDB.edit_language(user_id=query.from_user.id, language=callback_data["code"])
    await query.message.edit_text(text=instructions("en"))

@dp.callback_query_handler(language.filter(code='ru'), state=Language.start)
async def process_callback_language(query: CallbackQuery, callback_data: dict):
    await query.answer(cache_time=3)
    BotDB.edit_language(user_id=query.from_user.id, language=callback_data["code"])
    await query.message.edit_text(text=instructions("ru"))

def main():
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()