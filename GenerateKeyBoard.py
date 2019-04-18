from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import price_select
def Generate_markup():

    item = price_select.Conncet()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.one_time_keyboard=True

    for itm in item:
        markup.add(itm)

    return markup
