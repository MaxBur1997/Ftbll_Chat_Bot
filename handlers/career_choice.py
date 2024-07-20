from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import Command
from Chat_Bot_3_0.keyboards.prof_keyboards import make_row_keyboard


router = Router()

clubs = [
    "Арсенал",
    "Челси",
    "Манчестер Сити",
    "Ливерпуль"
]

class ChoiceProfile(StatesGroup):
    club_1 = State()
    club_2 = State()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Выберите команду 1: ", reply_markup=make_row_keyboard(clubs))
    await state.set_state(ChoiceProfile.club_1)

@router.message(ChoiceProfile.club_1, F.text.lower() == 'закрыть')
async def cmd_close(message: types.Message, state: FSMContext):
    await message.answer("Набор сброшен",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

@router.message(ChoiceProfile.club_1, F.text.in_(clubs))
async def club_1_chosen(message: types.Message, state: FSMContext):
    await state.update_data(club1=message.text)
    await message.answer("Выберите команду 2: ", reply_markup=make_row_keyboard(clubs))
    await state.set_state(ChoiceProfile.club_2)


@router.message(ChoiceProfile.club_1)
async def not_club_1_chosen(message: types.Message):
    await message.answer("Выберите команду 1: ", reply_markup=make_row_keyboard(clubs))


@router.message(ChoiceProfile.club_2, F.text.in_(clubs))
async def club_2_chosen(message: types.Message, state: FSMContext):
    club_data = await state.get_data()
    if club_data['club1'] == message.text:
        await message.answer("Выбрана та же команда\n")
        await message.answer("Выберите команду 2: ", reply_markup=make_row_keyboard(clubs))
        await state.set_state(ChoiceProfile.club_2)
    else:
        await message.answer(f"Команда №1: {club_data['club1']}\n"
                             f"Команда №2: {message.text}\n"
                             "Моя работа завершена. Чтобы продолжить введите команду /start",
                             reply_markup=types.ReplyKeyboardRemove())
        await state.clear()

@router.message(ChoiceProfile.club_2)
async def not_club_2_chosen(message: types.Message):
    await message.answer("Выберите команду 2: ", reply_markup=make_row_keyboard(clubs))