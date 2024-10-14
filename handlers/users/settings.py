from aiogram import types
from keyboards.default.default import setings_btn, language_set_btn
from states.all_states import current_menu
from utils.db_api.database import db

from loader import dp

@dp.message_handler(text="⚙️ Настройки")
async def settings(message: types.Message):
    await message.answer("<b>Выберите действие:</b>", reply_markup=setings_btn[db.check_language(message.from_user.id)], parse_mode="HTML")
    current_menu[message.from_user.id] = "settings"

@dp.message_handler(text="⚙️ Sozlamalar")
async def settingss(message: types.Message):
    await message.answer("<b>Harakat tanlang:</b>", reply_markup=setings_btn[db.check_language(message.from_user.id)], parse_mode="HTML")
    current_menu[message.from_user.id] = "settings"


@dp.message_handler(text="Изменить язык")
async def change_language(message: types.Message):
    await message.answer("<b>Выберите язык:</b>", reply_markup=language_set_btn[db.check_language(message.from_user.id)], parse_mode="HTML")
    current_menu[message.from_user.id] = "lng"

@dp.message_handler(text="🇷🇺 Русский")
async def russian(message: types.Message):
    db.language("RU", message.from_user.id)
    await message.answer("<b>✅ Готово</b>", reply_markup=setings_btn[db.check_language(message.from_user.id)], parse_mode="HTML")
    current_menu[message.from_user.id] = "settings"

@dp.message_handler(text="🇺🇿 O'zbekcha")
async def uzb(message: types.Message):
    db.language("UZ", message.from_user.id)
    await message.answer("<b>✅ Tayyor</b>", reply_markup=setings_btn[db.check_language(message.from_user.id)], parse_mode="HTML")
    current_menu[message.from_user.id] = "settings"

@dp.message_handler(text="Tilni o'zgartirish")
async def uz_change_lang(message: types.Message):
    await message.answer("<b>Tilni o'zgartirish</b>", reply_markup=language_set_btn[db.check_language(message.from_user.id)], parse_mode="HTML")
    current_menu[message.from_user.id] = "lng"