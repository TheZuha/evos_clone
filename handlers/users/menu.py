from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.apis.api import get_address_from_coordinates
from utils.db_api.database import db
from states.all_states import MenuState, current_menu, OrderState
from keyboards.default.default import create_category_buttons, create_products_buttons, tel, loc
from keyboards.inline.inline import create_basket_buttons, create_cart_buttons, cart_cb

from loader import dp


@dp.message_handler(lambda message: message.text in [category[1] for category in db.get_all_categories()], state=MenuState.category)
async def show_products(message: types.Message, state: FSMContext):
    lang = db.check_language(message.from_user.id)
    category_name = message.text
    await state.update_data(category_name=category_name)
    category_id = db.get_category_id_by_name(category_name)
    if category_id: 
        products_list = db.get_products_by_category_id(category_id)
        if products_list:
            reply_markup = create_products_buttons(products_list, lang)
            if lang == "RU":
                await message.answer("Выберите продукт:", reply_markup=reply_markup)
            else:
                await message.answer("Mahsulotni tanlang:", reply_markup=reply_markup)
            await MenuState.product.set()
        else:
            if lang == "RU":
                await message.answer("В этой категории пока нет продуктов.")
            else:
                await message.answer("Ushbu kategoriyada hali mahsulotlar yo'q.")
    else:
        if lang == "RU":
            await message.answer("Категория не найдена.")
        else:
            await message.answer("Kategoriya topilmadi.")

def convert_count_to_emoji(count):
    emoji_numbers = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣'
    }
    return ''.join(emoji_numbers[digit] for digit in str(count))


@dp.message_handler(lambda message: message.text in ["📥 Корзина", "📥 Savat"], state="*")
async def basket_ru(message: types.Message):
    chat_id = message.from_user.id
    lang = db.check_language(chat_id)
    basket_items = db.get_basket(chat_id)

    if not basket_items:
        if lang == "RU":
            await message.answer("Корзина пуста.")
        else:
            await message.answer("Savatcha bo'sh.")
        return


    total_price = db.calculate_total_price(chat_id)
    delivery_price = 12000
    final_price = total_price + delivery_price

    basket_text = ""
    
    for item in basket_items:
        print(item)
        product_name = item[2]
        count = item[3]
        product_price = item[1]
        count_emoji = convert_count_to_emoji(count)
        basket_text += f"{count_emoji} ✖️ {product_name}\n"


    if lang == "RU":
        basket_message = f"""
В корзине:
{basket_text}
Товары: {product_price} сум
Доставка: {delivery_price} сум
Итого: {final_price} сум
        """
    else:
        basket_message = f"""
Savatchada:
{basket_text}
Mahsulotlar: {product_price} so'm
Yetkazib berish: {delivery_price} so'm
Jami: {final_price} so'm
        """
    markup = create_basket_buttons(basket_items, lang)

    await message.answer(basket_message, reply_markup=markup)



@dp.message_handler(state=MenuState.product)
async def menuu(message: types.Message):
    product_name = message.text
    lang = db.check_language(message.from_user.id)
    data = db.get_products(product_name)
    image = data[0][4]
    description = data[0][2]
    price = data[0][3]
    caption = f"{description}\n\nNarxi: {price} so'm"
    await message.answer_photo(photo=image, caption=caption, reply_markup=create_cart_buttons(1, lang))
    await MenuState.join.set()
        # if lang == 'RU':
        #     await message.answer("Корзина пуста!")
        # else:
        #     await message.answer("Savatcha bo'sh!")


@dp.callback_query_handler(cart_cb.filter(action='decrease'), state="*")
async def decrease_quantity(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    quantity = int(callback_data['quantity'])
    if quantity > 0:
        quantity -= 1
    lang = db.check_language(query.from_user.id)
    await query.answer(f"{quantity} ta")
    await query.message.edit_reply_markup(create_cart_buttons(quantity, lang))
    await MenuState.join.set()

@dp.callback_query_handler(cart_cb.filter(action='increase'), state="*")
async def increase_quantity(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    quantity = int(callback_data['quantity'])
    quantity += 1
    lang = db.check_language(query.from_user.id)
    await query.answer(f"{quantity} ta")
    await query.message.edit_reply_markup(create_cart_buttons(quantity, lang))
    await MenuState.join.set()

@dp.callback_query_handler(cart_cb.filter(action='add_to_cart'), state=MenuState.join)
async def add_to_cart(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    chat_id = query.from_user.id
    lang = db.check_language(chat_id)
    data = await state.get_data()
    category_name = data.get("category_name")
    category_id = db.get_category_id_by_name(category_name)
    category_list = db.get_all_categories()
    reply_markup = create_category_buttons(category_list, lang)

    quantity = int(callback_data['quantity'])
    product_name = db.get_product_name_by_category_id(category_id)

    # Mahsulot narxini olamiz va uni integer formatga o'giramiz
    product_price_str = db.get_product_price_by_category_id(category_id)[0]
    product_price = int(product_price_str.replace(" ", ""))  # Probelni olib tashlab, narxni int formatiga o'tkazish

    total_price = product_price * quantity + 12000  # Narxni ko'paytirish

    if lang == "RU":
        await query.answer("Добавлен")
        await query.message.answer("Выберите одно из следующих", reply_markup=reply_markup)
    else:
        await query.answer("Qo'shildi")
        await query.message.answer("Quyidagilardan birini tanlang", reply_markup=reply_markup)
    
    db.insert_product_to_basket(product_name, quantity, total_price, chat_id)
    
    await query.message.delete()
    await MenuState.category.set()



@dp.callback_query_handler(lambda c: c.data.startswith("remove_"), state="*")
async def remove_product_from_baskett(callback_query: types.CallbackQuery):
    product_id = int(callback_query.data.split("_")[1])
    print(product_id)
    chat_id = callback_query.from_user.id
    db.remove_product_from_basket(chat_id, product_id)

    await callback_query.message.delete()
    await basket_ru(callback_query.message)
    

@dp.callback_query_handler(lambda c: c.data in ["back_RU", "back_UZ", "clear_RU", "clear_UZ"], state="*")
async def process_callbackk(callback_query: types.CallbackQuery):
    data = callback_query.data
    chat_id = callback_query.from_user.id
    lang = db.check_language(chat_id)
    all_category = db.get_all_categories()
    reply_markup = create_category_buttons(all_category, lang)

    if data in ["back_RU", "back_UZ"]:
        # Orqaga qaytish harakati (Bosh menyuga yoki oldingi menyuga qaytish)
        await callback_query.message.delete()
        if lang == "RU":
            await callback_query.message.answer("Выберите категорию.", reply_markup=reply_markup)
        else:
            await callback_query.message.answer("Bo'limni tanlang.", reply_markup=reply_markup)

    elif data in ["clear_RU", "clear_UZ"]:
        # Savatni tozalash
        db.delete_basket(chat_id)
        await callback_query.message.delete()
        if lang == "RU":
            await callback_query.message.answer("Корзина очищена.", reply_markup=reply_markup)
        else:
            await callback_query.message.answer("Savatcha tozalandi.", reply_markup=reply_markup)
    await MenuState.category.set()
    


@dp.callback_query_handler(lambda query: query.data in ["zakaz_UZ", "zakaz_RU"], state="*")
async def zakaz_qilish(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.from_user.id
    lang = db.check_language(chat_id)

    phone = db.get_contact(chat_id)
    
    if phone is None:
        if lang == "RU":
            await callback_query.message.answer("Отправьте телефон номер:", reply_markup=tel[lang])
        else:
            await callback_query.message.answer("Telefon raqamingizni kiriting:", reply_markup=tel[lang])
        await OrderState.waiting_for_phone.set()
    else:
        await state.update_data(phone=phone)
        if lang == "RU":
            await callback_query.message.answer("Отправьте свою локацию:", reply_markup=loc[lang])
        else:
            await callback_query.message.answer("Yetkazib berish manzilingizni kiriting:", reply_markup=loc[lang])
        await OrderState.waiting_for_address.set()



@dp.message_handler(state=OrderState.waiting_for_phone, content_types=types.ContentType.TEXT)
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    chat_id = message.from_user.id
    lang = db.check_language(chat_id)

    if lang == "RU":
        await message.answer("Отправьте свою локацию:", reply_markup=loc[lang])
    else:
        await message.answer("Yetkazib berish manzilingizni kiriting:", reply_markup=loc[lang])
    await OrderState.waiting_for_address.set()

@dp.message_handler(state=OrderState.waiting_for_address, content_types=types.ContentType.LOCATION)
async def process_address(message: types.Message, state: FSMContext):
    latitude = message.location.latitude
    longitude = message.location.longitude

    address = await get_address_from_coordinates(latitude, longitude)

    chat_id = message.from_user.id
    lang = db.check_language(chat_id)

    data = await state.get_data()
    phone = data.get("phone")
    
    basket_items = db.get_basket(chat_id)
    
    if not basket_items:
        if lang == "RU":
            await message.answer("Корзина пуста.")
        else:
            await message.answer("Savatcha bo'sh.")
        await state.finish()
        return
    
    for item in basket_items:
        print(item)
        product_name = item[2]
        total_price = item[1] * item[3]
        count = item[3]
        db.insert_order(product_name, count, total_price, chat_id, address, phone)
    
    all_category = db.get_all_categories()
    reply_markup = create_category_buttons(all_category, lang)
    
    if lang == "RU":
        await message.answer("Ваш заказ принят!", reply_markup=reply_markup)
    else:
        await message.answer("Buyurtmangiz qabul qilindi!", reply_markup=reply_markup)
    
    db.delete_basket(chat_id)
    
    await state.finish()


@dp.message_handler(text="🛍 Мои заказы")
async def my_orders(message: types.Message):
    orders = db.get_my_orders(message.from_user.id)
    
    print(orders)
    for order in orders:
        print(order)
        name = order[1]
        price = db.get_product_price_by_name(name)
        count = order[2]
        count_emoji = convert_count_to_emoji(count)
        total_price = order[3]
        location = order[6]
        await message.answer(f"""
Manzil: {location}
  
{count_emoji} ✖️ {name}
    
Mahsulotlar: {price[0]} so'm
Yetkazib berish: 12000 so'm
Jami: {total_price} so'm
""")
