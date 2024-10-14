from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.apis.api import chat_idd


menu = {
    'UZ': ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="🍴 Menyu")],
        [KeyboardButton(text="🛍 Mening buyurtmalarim")],
        [KeyboardButton(text="✍️ Fikr bildirish"), KeyboardButton(text="⚙️ Sozlamalar")]
    ]),
    'RU': ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="🍴 Меню")],
        [KeyboardButton(text="🛍 Мои заказы")],
        [KeyboardButton(text="✍️ Оставить отзыв"), KeyboardButton(text="⚙️ Настройки")]
    ])
}


feedback_no_contact = {
    'UZ': ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="📞Mening raqamim", request_contact=True)], 
        [KeyboardButton(text="⬅️ Ortga")]
    ]), 
    'RU': ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="📞Мой номер", request_contact=True)],
        [KeyboardButton(text="⬅️ Назад")]
    ])
}

feedback_yes_contact = {
    'UZ': ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="⬅️ Ortga")]
    ]),
    'RU': ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="⬅️ Назад")]
    ])
}


setings_btn = {
    "RU": ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="Изменить язык")],
        [KeyboardButton(text="⬅️ Назад")]
    ]),
    "UZ": ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="Tilni o'zgartirish")],
        [KeyboardButton(text="⬅️ Ortga")]
    ])
}


language_set_btn = {
    "RU": ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇺🇿 O'zbekcha")],
        [KeyboardButton(text="⬅️ Назад")]
    ]),
    "UZ": ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇺🇿 O'zbekcha")],
        [KeyboardButton(text="⬅️ Ortga")]
    ])
}



geo_location = {
    "RU": ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="🗺 Мои адреса")],
        [KeyboardButton(text="📍 Отправить геолокацию", request_location=True), KeyboardButton(text="⬅️ Назад")]
    ]),
    "UZ": ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="🗺 Mening manzillarim")],
        [KeyboardButton(text="📍 Geolokatsiyani yuborish", request_location=True), KeyboardButton(text="⬅️ Ortga")]
    ])
}



def create_location_buttons(locations, lang):
    my_manzil = {
        "RU": ReplyKeyboardMarkup(resize_keyboard=True, row_width=1),
        "UZ": ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    }

    btns_ru = []
    btns_uz = []

    for location in locations:
        print(location[0], location)
        btns_ru.append(KeyboardButton(text=location[0]))
        btns_uz.append(KeyboardButton(text=location[0]))

    btns_ru.append(KeyboardButton(text="⬅️ Назад"))
    btns_uz.append(KeyboardButton(text="⬅️ Ortga"))

    my_manzil["RU"].add(*btns_ru)
    my_manzil["UZ"].add(*btns_uz)

    return my_manzil[lang]

def create_category_buttons(categories, lang):
    my_categories = {
        "RU": ReplyKeyboardMarkup(resize_keyboard=True, row_width=2),
        "UZ": ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    }

    btns_ru = []
    btns_uz = []

    for category in categories:
        # print(category[0], category)
        btns_ru.append(KeyboardButton(text=category[1]))
        btns_uz.append(KeyboardButton(text=category[1]))

    btns_ru.append(KeyboardButton(text="⬅️ Назад"))
    btns_ru.append(KeyboardButton(text="📥 Корзина"))
    btns_uz.append(KeyboardButton(text="⬅️ Ortga"))
    btns_uz.append(KeyboardButton(text="📥 Savat"))

    my_categories["RU"].add(*btns_ru)
    my_categories["UZ"].add(*btns_uz)

    return my_categories[lang]

def create_products_buttons(products, lang):
    my_products = {
        "RU": ReplyKeyboardMarkup(resize_keyboard=True, row_width=2),
        "UZ": ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    }
    btns_ru = []
    btns_uz = []

    for product in products:
        print(product[0], product)
        btns_ru.append(KeyboardButton(text=product[1]))
        btns_uz.append(KeyboardButton(text=product[1]))

    btns_ru.append(KeyboardButton(text="⬅️ Назад"))
    btns_ru.append(KeyboardButton(text="📥 Корзина"))
    btns_uz.append(KeyboardButton(text="⬅️ Ortga"))
    btns_uz.append(KeyboardButton(text="📥 Savat"))

    my_products["RU"].add(*btns_ru)
    my_products["UZ"].add(*btns_uz)

    return my_products[lang]


confirm = {
    "RU": ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="✅ Да"), KeyboardButton(text="❌ Нет")],
        [KeyboardButton(text="⬅️ Назад")]
    ]),
    "UZ": ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="✅ Ha"), KeyboardButton(text="❌ Yo'q")],
        [KeyboardButton(text="⬅️ Ortga")]
    ])
}

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
admin_keyboard.add(KeyboardButton("Add Category"))
admin_keyboard.add(KeyboardButton("Add Product"))


tel = {
    "RU": ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📞 Мой номер", request_contact=True)]
    ], resize_keyboard=True),
    "UZ": ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📞 Mening raqamim", request_contact=True)]
    ], resize_keyboard=True)
}

loc = {
    "RU": ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📍 Отправить геолокацию", request_location=True)]
    ], resize_keyboard=True),
    "UZ": ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📍 Geolokatsiyani yuborish", request_location=True)]
    ], resize_keyboard=True)
}