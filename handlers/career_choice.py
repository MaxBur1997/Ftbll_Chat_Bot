from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import Command
from Chat_Bot_3_0.keyboards.prof_keyboards import make_row_keyboard


router = Router()

available_jobs = [
    "Программист",
    "Дизайнер",
    "Маркетолог"
]

available_grades = ['Junior', 'Middle', 'Senior']

class ChoiceProfile(StatesGroup):
    job = State()
    grade = State()


@router.message(Command("prof"))
async def cmd_prof(message: types.Message, state: FSMContext):
    await message.answer("Выберите профессию", reply_markup=make_row_keyboard(available_jobs))
    await state.set_state(ChoiceProfile.job)

@router.message(ChoiceProfile.job, F.text.lower() == 'закрыть')
async def cmd_close_job(message: types.Message, state: FSMContext):
    await message.answer("Набор сброшен",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

@router.message(ChoiceProfile.job, F.text.in_(available_jobs))
async def prof_chosen(message: types.Message, state: FSMContext):
    await state.update_data(profession=message.text)
    await message.answer("Выберите уровень", reply_markup=make_row_keyboard(available_grades))
    await state.set_state(ChoiceProfile.grade)

@router.message(ChoiceProfile.job)
async def not_prof_chosen(message: types.Message):
    await message.answer("Выберите профессию", reply_markup=make_row_keyboard(available_jobs))

@router.message(ChoiceProfile.grade, F.text.lower() == 'закрыть')
async def cmd_close_grade(message: types.Message, state: FSMContext):
    await message.answer("Набор сброшен",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

@router.message(ChoiceProfile.grade, F.text.in_(available_grades))
async def grade_chosen(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(f"Ваша профессия: {user_data['profession']}\n"
                         f"Ваш уровень: {message.text}\n"
                         "Моя работа завершена. Чтобы продолжить введите команду /start или скажите мне 'Привет'",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

@router.message(ChoiceProfile.grade)
async def not_grade_chosen(message: types.Message):
    await message.answer("Выберите уровень", reply_markup=make_row_keyboard(available_grades))