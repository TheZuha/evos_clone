from aiogram.dispatcher.filters.state import StatesGroup, State

current_menu = {}


class FeedbackState(StatesGroup):
    contact = State()
    text = State()


class LocationState(StatesGroup):
    location = State()
    confirm = State()
    time = State()

class CategoryState(StatesGroup):
    name = State()

class ProductState(StatesGroup):
    name = State()
    description = State()
    price = State()
    category_id = State()
    photo = State()


class ManzilState(StatesGroup):
    address = State()

class MenuState(StatesGroup):
    category = State()
    product = State()
    join = State()


class OrderState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_address = State()