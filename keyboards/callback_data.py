from ast import Call
from aiogram.utils.callback_data import CallbackData

language =  CallbackData("language", "code") # language:uz
chapter_data = CallbackData("chapter", "chapter_id") # chapter:1
pagination = CallbackData("pagination", "key") # pagination:forward