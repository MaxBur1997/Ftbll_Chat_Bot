from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import Command
from Chat_Bot_3_0.keyboards.prof_keyboards import make_row_keyboard


router = Router()

champs = [
    "АПЛ",
    "Ла Лига",
    "Серия А",
    "Бундеслига"
]

clubs = []

clubs_apl = [
    "Арсенал",
    "Челси",
    "Манчестер Сити",
    "Ливерпуль"
]

clubs_la_liga = [
    "Барселона",
    "Реал Мадрид",
    "Валенсия",
    "Осасуна"
]

clubs_seria_a = [
    "Милан",
    "Интер",
    "Рома",
    "Ювентус"
]

clubs_bundes = [
    "Бавария",
    "Буруссия Д",
    "Байер",
    "Штутгарт"
]

class ChoiceProfile(StatesGroup):
    championship = State()
    club_1 = State()
    club_2 = State()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Выберите чемпионат: ", reply_markup=make_row_keyboard(champs))
    await state.set_state(ChoiceProfile.championship)

@router.message(ChoiceProfile.championship, F.text.lower() == 'закрыть')
async def cmd_close(message: types.Message, state: FSMContext):
    await message.answer("Набор сброшен\n"
                         "Чтобы начать заново, введите команду /start",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

@router.message(ChoiceProfile.championship, F.text.in_(champs))
async def champ_chosen(message: types.Message, state: FSMContext):
    global clubs
    if message.text == "АПЛ":
        clubs = clubs_apl
    if message.text == "Ла Лига":
        clubs = clubs_la_liga
    if message.text == "Серия А":
        clubs = clubs_seria_a
    if message.text == "Бундеслига":
        clubs = clubs_bundes
    await state.update_data(champ=message.text)
    await message.answer("Выберите команду 1: ", reply_markup=make_row_keyboard(clubs))
    await state.set_state(ChoiceProfile.club_1)

@router.message(ChoiceProfile.championship)
async def not_champ_chosen(message: types.Message):
    await message.answer("Выберите чемпионат из списка: ", reply_markup=make_row_keyboard(champs))

@router.message(ChoiceProfile.club_1, F.text.lower() == 'закрыть')
async def cmd_close(message: types.Message, state: FSMContext):
    await message.answer("Набор сброшен\n"
                         "Чтобы начать заново, введите команду /start",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.clear()
@router.message(ChoiceProfile.club_1)
async def club_1_chosen(message: types.Message, state: FSMContext):
    await state.update_data(club1=message.text)
    await message.answer("Выберите команду 2: ", reply_markup=make_row_keyboard(clubs))
    await state.set_state(ChoiceProfile.club_2)

@router.message(ChoiceProfile.club_2, F.text.lower() == 'закрыть')
async def cmd_close(message: types.Message, state: FSMContext):
    await message.answer("Набор сброшен.\n"
                         "Чтобы начать заново, введите команду /start",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.clear()
@router.message(ChoiceProfile.club_2)
async def club_2_chosen(message: types.Message, state: FSMContext):
    club_data = await state.get_data()
    if club_data['club1'] == message.text:
        await message.answer("Выбрана та же команда\n")
        await message.answer("Выберите команду 2: ", reply_markup=make_row_keyboard(clubs))
        await state.set_state(ChoiceProfile.club_2)
    else:
        if club_data['club1'] in clubs and message.text in clubs:
            await message.answer(f"Чемпионат: {club_data['champ']}\n"
                                 f"Команда №1: {club_data['club1']}\n"
                                 f"Команда №2: {message.text}\n"
                                 "Моя работа завершена. Чтобы продолжить введите команду /start",
                                 reply_markup=types.ReplyKeyboardRemove())
            await state.clear()
        else:
            await message.answer("Некорректный выбор команд.\n"
                                 "Пожалуйста, начните заново, введя команду /start, и выберите команды из предлагаемого списка",
                                 reply_markup=types.ReplyKeyboardRemove())
            await state.clear()
