from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard(buttons: list, btn=KeyboardButton(text="Закрыть")) -> ReplyKeyboardMarkup:
    row1 = [KeyboardButton(text=button) for button in buttons[:len(buttons)//10]]
    row2 = [KeyboardButton(text=button) for button in buttons[len(buttons)//10:len(buttons)*2//10]]
    row3 = [KeyboardButton(text=button) for button in buttons[len(buttons)*2//10:len(buttons)*3//10]]
    row4 = [KeyboardButton(text=button) for button in buttons[len(buttons) * 3 // 10:len(buttons) * 4 // 10]]
    row5 = [KeyboardButton(text=button) for button in buttons[len(buttons) * 4 // 10:len(buttons) * 5 // 10]]
    row6 = [KeyboardButton(text=button) for button in buttons[len(buttons) * 5 // 10:len(buttons) * 6 // 10]]
    row7 = [KeyboardButton(text=button) for button in buttons[len(buttons) * 6 // 10:len(buttons) * 7 // 10]]
    row8 = [KeyboardButton(text=button) for button in buttons[len(buttons) * 7 // 10:len(buttons) * 8 // 10]]
    row9 = [KeyboardButton(text=button) for button in buttons[len(buttons) * 8 // 10:len(buttons) * 9 // 10]]
    row10 = [KeyboardButton(text=button) for button in buttons[len(buttons) * 9 // 10:]]
    return ReplyKeyboardMarkup(keyboard=[row1, row2, row3, row4, row5, row6, row7, row8, row9, row10,[btn]], resize_keyboard=True)