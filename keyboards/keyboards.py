from aiogram import types


button1 = types.KeyboardButton(text='Получить данные')
button2 = types.KeyboardButton(text='Закрыть')

keyboard1 = [[button1, button2]]

kb1 = types.ReplyKeyboardMarkup(keyboard=keyboard1,
                                resize_keyboard=True)