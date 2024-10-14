from aiogram import types
from data.config import ADMINS
from states.all_states import CategoryState, ProductState
from utils.db_api.database import db
from keyboards.default.default import admin_keyboard, create_category_buttons
from aiogram.dispatcher import FSMContext

from loader import dp


def is_admin(chat_id):
    return str(chat_id) in ADMINS

@dp.message_handler(commands=["admin"], state="*")
async def admin_panel(message: types.Message, state: FSMContext):
    await state.finish()
    if is_admin(message.from_user.id):
        if db.check_language(message.from_user.id) == "RU":
            await message.answer("Админ панель:", reply_markup=admin_keyboard)
        else:
            await message.answer("Admin panel:", reply_markup=admin_keyboard)
    else:
        await message.answer("Siz admin emassiz!")


@dp.message_handler(lambda message: message.text == "Add Category", state="*")
async def add_category_start(message: types.Message):
    if is_admin(message.from_user.id):
        if db.check_language(message.from_user.id) == "RU":
            await message.answer("Введите название категории:")
        else:
            await message.answer("Kategoriya ismini kiriting:")
        await CategoryState.name.set()


@dp.message_handler(state=CategoryState.name)
async def process_category_name(message: types.Message, state: FSMContext):
    category_name = message.text
    all_category = db.get_all_categories()
    existing_category_names = [category[1].lower() for category in all_category]
    if category_name.lower() in existing_category_names:
        if db.check_language(message.from_user.id) == "RU":
            await message.answer(f"Категория с именем '{category_name}' уже существует. Введите другое название.")
        else:
            await message.answer(f"'{category_name}' nomli kategoriya mavjud. Iltimos, boshqa nom kiriting.")
    else:
        lang = db.check_language(message.from_user.id)
        db.insert_category(category_name)
        all_category = db.get_all_categories()

        reply_markup = create_category_buttons(all_category, lang)
        if db.check_language(message.from_user.id) == "RU":
            await message.answer(f"Категория '{category_name}' успешно добавлена.", reply_markup=reply_markup)
        else:
            await message.answer(f"Kategoriya '{category_name}' muvaffaqiyatli qo'shildi.", reply_markup=reply_markup)
        await state.finish()


@dp.message_handler(text="Add Product", state="*")
async def add_product_start(message: types.Message):
    if is_admin(message.from_user.id):
        if db.check_language(message.from_user.id) == "RU":
            await message.answer("Введите название продукта:")
        else:
            await message.answer("Mahsulot nomini kiriting:")
        await ProductState.name.set()


@dp.message_handler(state=ProductState.name)
async def process_product_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    if db.check_language(message.from_user.id) == "RU":
        await message.answer("Введите описание продукта:")
    else:
        await message.answer("Mahsulot tavsifini kiriting:")
    await ProductState.description.set()

@dp.message_handler(state=ProductState.description)
async def process_product_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    if db.check_language(message.from_user.id) == "RU":
        await message.answer("Введите цену продукта:")
    else:
        await message.answer("Mahsulot narxini kiriting:")
    await ProductState.price.set()

@dp.message_handler(state=ProductState.price)
async def process_product_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    all_category = db.get_all_categories()
    lang = db.check_language(message.from_user.id)
    reply_markup = create_category_buttons(all_category, lang)
    if db.check_language(message.from_user.id) == "RU":
        await message.answer("Выберите категорию:", reply_markup=reply_markup)
    else:
        await message.answer("Kategoriyani tanlang:", reply_markup=reply_markup)
    await ProductState.category_id.set()

@dp.message_handler(state=ProductState.category_id)
async def process_product_photo(message: types.Message, state: FSMContext):
    category_name = message.text
    category_id = db.get_category_id_by_name(category_name)
    if category_id:
        await state.update_data(category_id=category_id)
        if db.check_language(message.from_user.id) == "RU":
            await message.answer("Отправьте фото продукта:")
        else:
            await message.answer("Mahsulot rasmini yuboring:")
        await ProductState.next()
    else:
        if db.check_language(message.from_user.id) == "RU":
            await message.answer("Неверная категория, попробуйте снова:")
        else:
            await message.answer("Noto'g'ri kategoriya, qaytadan urinib ko'ring:")
        await ProductState.category_id.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=ProductState.photo)
async def process_product_photo(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(image=file_id)
    data = await state.get_data()
    print(data)
    db.insert_product(data['name'], data['description'], data['price'], data['image'], data['category_id'])
    await state.finish()
    if db.check_language(message.from_user.id) == "RU":
        await message.answer("Продукт успешно добавлен.")
    else:
        await message.answer("Mahsulot muvaffaqiyatli qo'shildi.")
