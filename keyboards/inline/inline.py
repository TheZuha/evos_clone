from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

vaqt = {
    'UZ': InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Hozir", callback_data="now_UZ"), InlineKeyboardButton(text="Boshqa vaqtda", callback_data="after_UZ")]
    ]),
    'RU': InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сейчас", callback_data="now_RU"), InlineKeyboardButton(text="В другое время", callback_data="after_RU")]
    ])
}

cart_cb = CallbackData('cart', 'action', 'quantity')

def create_cart_buttons(quantity, lang):
    if lang == "RU":
        decrease_text = "-"
        increase_text = "+"
        add_to_cart_text = "📥 Добавить в корзину"
    else:
        decrease_text = "-"
        increase_text = "+"
        add_to_cart_text = "📥 Savatga qo'shish"
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=decrease_text, callback_data=cart_cb.new(action='decrease', quantity=quantity)),
            InlineKeyboardButton(text=str(quantity), callback_data='ignore'),
            InlineKeyboardButton(text=increase_text, callback_data=cart_cb.new(action='increase', quantity=quantity))
        ],
        [
            InlineKeyboardButton(text=add_to_cart_text, callback_data=cart_cb.new(action='add_to_cart', quantity=quantity))
        ]
    ])


def create_basket_buttons(basket_items, lang):
    markup = InlineKeyboardMarkup()
    
    for item in basket_items:
        print(item)
        product_name = item[2]
        callback_data = f"remove_{item[0]}"
        markup.add(InlineKeyboardButton(text=f"❌ {product_name}", callback_data=callback_data))
    
    if lang == "RU":
        markup.add(
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_RU"),
            InlineKeyboardButton(text="🚖 Оформить заказ", callback_data="zakaz_RU")
        )
        markup.add(InlineKeyboardButton(text="🗑️ Очистить корзину", callback_data="clear_RU"))
    else:
        markup.add(
            InlineKeyboardButton(text="⬅️ Ortga", callback_data="back_UZ"),
            InlineKeyboardButton(text="🚖 Buyurtma qilish", callback_data="zakaz_UZ")
        )
        markup.add(InlineKeyboardButton(text="🗑️ Savatni tozalash", callback_data="clear_UZ"))
    
    return markup