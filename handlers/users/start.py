from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.db_api.database import db
from keyboards.default.default import menu, setings_btn, geo_location
from states.all_states import current_menu, LocationState, CategoryState, ProductState, ManzilState, MenuState, FeedbackState
from aiogram.dispatcher import FSMContext

from loader import dp



@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id in db.all_chat_id():
        pass
    else:
        db.insert_user(message.from_user.id, "RU")
    if db.check_language(message.from_user.id) == "RU":
        await message.answer(text="Выберите одно из следующих", reply_markup=menu[db.check_language(message.from_user.id)])
        current_menu[message.from_user.id] = 'main'
    else:
        await message.answer(text="Quyidagilardan birini tanlang", reply_markup=menu[db.check_language(message.from_user.id)])
        current_menu[message.from_user.id] = 'main'



@dp.message_handler(text="⬅️ Назад")
async def go_back(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in current_menu:
        print(1)
        if current_menu[user_id] == "feedback":
            await state.finish()
            await message.answer(text="Выберите одно из следующих", reply_markup=menu[db.check_language(message.from_user.id)])
            current_menu[user_id] = "main"
        elif current_menu[user_id] == "settings":
            await state.finish()
            await message.answer(text="Выберите одно из следующих", reply_markup=menu[db.check_language(message.from_user.id)])
            current_menu[user_id] = "main"
        elif current_menu[user_id] == "lng":
            await message.answer("Выберите действие:", reply_markup=setings_btn[db.check_language(message.from_user.id)])
            current_menu[user_id] = "settings"
        elif current_menu[message.from_user.id] == "location":
            print(2)
            await state.finish()
            await message.answer(text="Выберите одно из следующих", reply_markup=menu[db.check_language(message.from_user.id)])
            current_menu[user_id] = "main"
        elif current_menu[user_id] == "confirm":
            await message.answer(text="Отправьте 📍 геолокацию или выберите адрес доставки", reply_markup=geo_location[db.check_language(message.from_user.id)])
            current_menu[user_id] = "location"
    else:
        print(f"{user_id} no in {current_menu}")

            

@dp.message_handler(text="⬅️ Ortga")
async def back_uz(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in current_menu:
        await state.finish()
        if current_menu[user_id] == "feedback":
            await message.answer(text="Quyidagilardan birini tanlang", reply_markup=menu[db.check_language(message.from_user.id)])
            current_menu[message.from_user.id] = 'main'
            await state.finish()
        elif current_menu[user_id] == "settings":
            await message.answer(text="Quyidagilardan birini tanlang", reply_markup=menu[db.check_language(message.from_user.id)])
            current_menu[message.from_user.id] = 'main'
            await state.finish()
        elif current_menu[user_id] == "lng":
            await message.answer("<b>Harakat tanlang:</b>", reply_markup=setings_btn[db.check_language(message.from_user.id)], parse_mode="HTML")
            current_menu[message.from_user.id] = "settings"
        elif current_menu[message.from_user.id] == "location":
            await message.answer(text="Quyidagilardan birini tanlang", reply_markup=menu[db.check_language(message.from_user.id)])
            current_menu[message.from_user.id] = 'main'
            await state.finish()
        elif current_menu[user_id] == "confirm":
            await message.answer(text="📍 Geolokatsiyani yuboring yoki yetkazib berish manzilini tanlang", reply_markup=geo_location[db.check_language(message.from_user.id)])
            current_menu[user_id] = "location"
    else:
        print(f"{user_id} no in {current_menu}")



        