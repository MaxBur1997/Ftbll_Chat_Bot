from aiogram import Router, types, F
from aiogram.filters.command import Command
from Chat_Bot_3_0.keyboards.keyboards import kb1
from Chat_Bot_3_0.random_fox import fox


router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я эхобот на aiogram 3. Отправь мне любое сообщение, и я повторю его.",
                         reply_markup=kb1)

@router.message(Command("fox"))
@router.message(Command("лиса"))
@router.message(F.text.lower() == 'покажи лису')
async def cmd_fox(message: types.Message):
    name = message.chat.first_name
    img_fox = fox()
    await message.answer(f'Держи лису, {name}')
    await message.answer_photo(photo=img_fox)
    #await bot.send_photo(message.from_user.id, photo=img_fox)

@router.message(F.text)
async def echo(message: types.Message):
    name = message.chat.first_name
    if 'привет' in message.text.lower():
        await message.answer(f'Привет, {name}', reply_markup=kb1)
    elif 'пока' in message.text.lower():
        await message.answer(f'Пока, {name}')
    elif 'инфо' in message.text.lower():
        name_data = message.chat.first_name
        id_data = message.chat.id
        await message.answer(f'Ваш никнейм: {name_data}\n'
                             f'ID чата: {id_data}')
    elif 'стоп' in message.text.lower():
        await message.answer("Моя работа остановлена. Чтобы продолжить введите команду /start или скажите мне 'Привет'",
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer(message.text)