import datetime
import sqlite3
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from utils.db_api.database import db
from keyboards.default.default import create_category_buttons, create_location_buttons, geo_location, confirm
from keyboards.inline.inline import vaqt
from utils.apis.api import chat_idd, get_address_from_coordinates
from states.all_states import LocationState, current_menu, ManzilState, MenuState

from loader import dp

@dp.message_handler(text="🍴 Меню")
async def geo(message: types.Message):
    await message.answer("Отправьте 📍 геолокацию или выберите адрес доставки", reply_markup=geo_location[db.check_language(message.from_user.id)])
    await LocationState.location.set()
    current_menu[message.from_user.id] = "location"
    db.delete_basket(message.from_user.id)

@dp.message_handler(text="🍴 Menyu")
async def geo_uz(message: types.Message):
    await message.answer("📍 Geolokatsiyani yuboring yoki yetkazib berish manzilini tanlang", reply_markup=geo_location[db.check_language(message.from_user.id)])
    await LocationState.location.set()
    current_menu[message.from_user.id] = "location"
    db.delete_basket(message.from_user.id)



@dp.message_handler(content_types=types.ContentType.LOCATION, state=LocationState.location)
async def handle_location(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    chat_id = message.from_user.id

    address = await get_address_from_coordinates(latitude, longitude)

    # Manzilni ma'lumotlar bazasidan tekshirib chiqamiz
    existing_address = db.get_location_by_address(chat_id, address)

    if existing_address:
        # Manzil mavjud bo'lsa, tasdiqlash
        confirmation_text = (
            f"Адрес, по которому вы хотите заказать: {address} Вы подтверждаете этот адрес?"
            if db.check_language(chat_id) == "RU"
            else f"Buyurtma bermoqchi bo'lgan manzil: {address} Ushbu manzilni tasdiqlaysizmi?"
        )
    else:
        # Manzil mavjud bo'lmasa, uni qo'shamiz va tasdiqlash
        try:
            db.insert_location(chat_id, address)
            confirmation_text = (
                f"Адрес, по которому вы хотите заказать: {address} Вы подтверждаете этот адрес?"
                if db.check_language(chat_id) == "RU"
                else f"Buyurtma bermoqchi bo'lgan manzil: {address} Ushbu manzilni tasdiqlaysizmi?"
            )
        except sqlite3.IntegrityError:
            # Agar manzil hali mavjud bo'lsa, xato xabari
            confirmation_text = (
                f"Адрес, по которому вы хотите заказать: {address} Уже существует в базе данных."
                if db.check_language(chat_id) == "RU"
                else f"Buyurtma bermoqchi bo'lgan manzil: {address} Baza ma'lumotlarida allaqachon mavjud."
            )

    # Tasdiqlash uchun reply_markup
    lang = db.check_language(chat_id)
    await message.reply(confirmation_text, reply_markup=confirm[lang])

    current_menu[chat_id] = "confirm"
    await LocationState.confirm.set()





@dp.message_handler(text=["✅ Да", "✅ Ha"], state=LocationState.confirm)
async def confirm_address(message: types.Message):
    if db.check_language(message.from_user.id) == "UZ":
        await message.answer("<b>Yetkazib berish vaqtini tanlang</b>", parse_mode="HTML", reply_markup=vaqt[db.check_language(message.from_user.id)])
    else:
        await message.answer("<b>Выберите время доставки</b>", parse_mode="HTML", reply_markup=vaqt[db.check_language(message.from_user.id)])
    await LocationState.time.set()

@dp.callback_query_handler(lambda c: c.data.startswith("now"), state=LocationState.time)
async def set_time(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    all_category = db.get_all_categories()
    lang = call.data.split('_')[1]
    chat_id = call.from_user.id
    reply_markup = create_category_buttons(all_category, lang)
    if db.check_language(chat_id) == "UZ":
        await call.message.answer("<b>Kunduzgi menu 10:01 dan 06:30 gacha</b>", parse_mode="HTML")
        await call.message.answer("Bo'limni tanlang.", reply_markup=reply_markup)
    else:
        await call.message.answer("<b>Меню Дневной с 10:01 до 06:30</b>", parse_mode="HTML")
        await call.message.answer("Выберите категорию.", reply_markup=reply_markup)
    await call.message.delete()
    await MenuState.category.set()


@dp.message_handler(lambda message: message.text in ["🗺 Мои адреса", "🗺 Mening manzillarim"], state="*")
async def adresa(message: types.Message, state: FSMContext):
    await state.finish()
    chat_id = message.from_user.id
    locations = db.get_location(chat_id)

    lang = db.check_language(message.from_user.id)

    reply_markup = create_location_buttons(locations, lang)

    if lang == "RU":
        await message.answer("Выберите адрес доставки", reply_markup=reply_markup)
    else:
        await message.answer("Yetkazib berish manzilni tanlang", reply_markup=reply_markup)
    await ManzilState.address.set()


@dp.message_handler(state=ManzilState.address)
async def adrs(message: types.Message, state: FSMContext):
    if db.check_language(message.from_user.id) == "UZ":
        await message.answer("<b>Yetkazib berish vaqtini tanlang</b>", parse_mode="HTML", reply_markup=vaqt[db.check_language(message.from_user.id)])
    else:
        await message.answer("<b>Выберите время доставки</b>", parse_mode="HTML", reply_markup=vaqt[db.check_language(message.from_user.id)])
    await LocationState.time.set()