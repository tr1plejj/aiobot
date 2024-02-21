from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

make_offer_kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Сделать заказ')
    ]
])


order_n_cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True,  one_time_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Заказать'),
        KeyboardButton(text='Отмена')
    ]
])


cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Отмена')
    ]
])
