from aiogram import types
from aiogram.dispatcher import FSMContext
from states.all_states import FeedbackState, current_menu
from utils.db_api.database import db
from keyboards.default.default import feedback_no_contact, feedback_yes_contact, menu

from loader import dp, bot

@dp.message_handler(text="✍️ Оставить отзыв")
async def feddback(message: types.Message): 
    contact = db.get_contact(message.from_user.id)
    if contact is not None:
        await message.answer("Отправьте ваши отзывы", reply_markup=feedback_yes_contact[db.check_language(message.from_user.id)])
        await FeedbackState.text.set()
        current_menu[message.from_user.id] = "feedback"
    else:
        await message.answer("Поделитесь контактом для дальнейшего связи с Вами", reply_markup=feedback_no_contact[db.check_language(message.from_user.id)])
        await FeedbackState.contact.set()
        current_menu[message.from_user.id] = "feedback"

@dp.message_handler(text="✍️ Fikr bildirish")
async def feed_back(message: types.Message):
    contact = db.get_contact(message.from_user.id)
    if contact is not None:
        await message.answer("Fikringizni yuboring", reply_markup=feedback_yes_contact[db.check_language(message.from_user.id)])
        await FeedbackState.text.set()
        current_menu[message.from_user.id] = "feedback"
    else:
        await message.answer("Siz bilan keyingi muloqot uchun kontaktingizni baham ko'ring", reply_markup=feedback_no_contact[db.check_language(message.from_user.id)])
        await FeedbackState.contact.set()
        current_menu[message.from_user.id] = "feedback"
    

@dp.message_handler(state=FeedbackState.contact, content_types=['contact'])
async def contactt(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    chat_id = message.from_user.id
    if message.contact:
        if db.check_language(chat_id) == "RU":
            await message.answer("Отправьте ваши отзывы", reply_markup=feedback_yes_contact[db.check_language(message.from_user.id)])
        else:
            await message.answer("Fikringizni yuboring", reply_markup=feedback_yes_contact[db.check_language(message.from_user.id)])
        current_menu[message.from_user.id] = "feedback"
        db.update_contact(contact, chat_id)
        await FeedbackState.text.set()
    else:
        if db.check_language(chat_id) == "RU":
            await message.answer("Поделитесь контактом для дальнейшего связи с Вами", reply_markup=feedback_no_contact[db.check_language(message.from_user.id)])
            current_menu[message.from_user.id] = "feedback"
        else:
            await message.answer("Siz bilan keyingi muloqot uchun kontaktingizni baham ko'ring", reply_markup=feedback_no_contact[db.check_language(message.from_user.id)])
            current_menu[message.from_user.id] = "feedback"

@dp.message_handler(state=FeedbackState.text, content_types=types.ContentType.ANY)
async def feedback_text(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await message.answer(text="Выберите одно из следующих", reply_markup=menu[db.check_language(message.from_user.id)])
        current_menu[message.from_user.id] = 'main'
        await state.finish()
    elif message.text == "⬅️ Ortga":
        await message.answer(text="Quyidagilardan birini tanlang", reply_markup=menu[db.check_language(message.from_user.id)])
        current_menu[message.from_user.id] = 'main'
        await state.finish()
    else:
        if message.content_type == 'text':
            otziv = message.text
            chat_id = message.from_user.id
            full_name = message.from_user.full_name
            username = message.from_user.username
            phone_number = db.get_contact(chat_id)
            caption = f"""
Пользователь отправил отзыв:

Имя и Фамилия: {full_name}
Имя пользователя: @{username}
Телефон номер: {phone_number}

Отзыв: <b>{otziv}</b>
"""
            await state.finish()
            current_menu[message.from_user.id] = "menu"
            if db.check_language(message.from_user.id) == "RU":
                await message.answer("Спасибо за ваш отзыв", reply_markup=menu[db.check_language(message.from_user.id)])
            else:
                await message.answer("Fikr-mulohazangiz uchun rahmat", reply_markup=menu[db.check_language(message.from_user.id)])
            await bot.send_message(846986401, caption, "HTML")
        else:
            if db.check_language(message.from_user.id) == "RU":
                await message.answer("Отправьте ваши отзывы", reply_markup=feedback_yes_contact[db.check_language(message.from_user.id)])
            else:
                await message.answer("Fikringizni yuboring", reply_markup=feedback_yes_contact[db.check_language(message.from_user.id)])
