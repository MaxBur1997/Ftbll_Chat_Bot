from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard(buttons: list, btn=KeyboardButton(text="Закрыть")) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=button) for button in buttons]
    return ReplyKeyboardMarkup(keyboard=[row, [btn]], resize_keyboard=True)