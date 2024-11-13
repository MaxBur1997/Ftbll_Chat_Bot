from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import Command
from keyboards.prof_keyboards import make_row_keyboard
from Parser.Parser import pars
from keyboards.keyboards import kb1


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
    "Ливерпуль",
    "Борнмут",
    "Астон Вилла",
    "Брентфорд",
    "Брайтон",
    "Кристал Пэлас",
    "Эвертон",
    "Фулхэм",
    "Ипсвич",
    "Лестер",
    "Манчестер Юнайтед",
    "Ньюкасл",
    "Ноттингем Форест",
    "Саутгемптон",
    "Тоттенхэм",
    "Вест Хэм",
    "Вулверхэмптон"]

clubs_la_liga = [
    "Барселона",
    "Реал Мадрид",
    "Валенсия",
    "Осасуна",
    "Сельта",
    "Атлетик",
    "Жирона",
    "Бетис",
    "Атлетико",
    "Эспаньол",
    "Хетафе",
    "Алавес",
    "Лас-Пальмас",
    "Леганес",
    "Мальорка",
    "Райо Вальекано",
    "Реал Сосьедад",
    "Вальядолид",
    "Севилья",
    "Вильярреал"
]

clubs_seria_a = [
    "Милан",
    "Интер",
    "Рома",
    "Ювентус",
    "Аталанта",
    "Болонья",
    "Кальяри",
    "Комо",
    "Эмполи",
    "Фиорентина",
    "Дженоа",
    "Лацио",
    "Лечче",
    "Монца",
    "Наполи",
    "Парма",
    "Торино",
    "Удинезе",
    "Венеция",
    "Верона"
]

clubs_bundes = [
    "Бавария",
    "Боруссия Д",
    "Байер",
    "Штутгарт",
    "Аугсбург",
    "Бохум",
    "Боруссия М",
    "Айнтрахт Ф",
    "Фрайбург",
    "Хайденхайм",
    "Хоффенхайм",
    "Хольштайн Киль",
    "Майнц",
    "РБ Лейпциг",
    "Санкт-Паули",
    "Унион Берлин",
    "Вердер",
    "Вольфсбург"
]

class ChoiceProfile(StatesGroup):
    championship = State()
    club_1 = State()
    club_2 = State()
    pars = State()

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
    await message.answer("Выберите команду хозяев: ", reply_markup=make_row_keyboard(sorted(clubs)))
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
    await message.answer("Выберите команду гостей: ", reply_markup=make_row_keyboard(sorted(clubs)))
    await state.set_state(ChoiceProfile.club_2)

@router.message(ChoiceProfile.club_2, F.text.lower() == 'закрыть')
async def cmd_close(message: types.Message, state: FSMContext):
    await message.answer("Набор сброшен.\n"
                         "Чтобы начать заново, введите команду /start",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

@router.message(ChoiceProfile.pars, F.text.lower() == 'закрыть')
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
        await message.answer("Выберите команду гостей: ", reply_markup=make_row_keyboard(clubs))
        await state.set_state(ChoiceProfile.club_2)
    else:
        if club_data['club1'] in clubs and message.text in clubs:
            await message.answer(f"Чемпионат: {club_data['champ']}\n"
                                 f"Команда хозяев: {club_data['club1']}\n"
                                 f"Команда гостей: {message.text}\n"
                                 "Выбор команд завершен. Чтобы продолжить нажмите на кнопку 'Получить данные'",
                                 reply_markup=kb1)
            await state.update_data(club2=message.text)
            await state.set_state(ChoiceProfile.pars)
        else:
            await message.answer("Некорректный выбор команд.\n"
                                 "Пожалуйста, начните заново, введя команду /start, и выберите команды из предлагаемого списка",
                                 reply_markup=types.ReplyKeyboardRemove())
            await state.clear()

@router.message(ChoiceProfile.pars)
async def cmd_pars(message: types.Message, state: FSMContext):
    data_for_pars = await state.get_data()
    res_pars = pars(data_for_pars['champ'], data_for_pars['club1'], data_for_pars['club2'])
    await message.answer(f"Количество травмированных у хозяев: {res_pars[0]}\n"
                         f"Количество дисквалификаций у хозяев: {res_pars[1]}\n"
                         f"Количество травмированных у гостей: {res_pars[2]}\n"
                         f"Количество дисквалификаций у гостей: {res_pars[3]}\n"
                         f"Место хозяев в турнирной таблице: {res_pars[4]}\n"
                         f"Место гостей в турнирной таблице: {res_pars[5]}\n"
                         f"Количество очков хозяев, набранных в домашних матчах: {res_pars[6]}\n"
                         f"Количество очков гостей, набранных в гостевых матчах: {res_pars[7]}\n"
                         f"Количество матчей хозяев: {res_pars[8]}\n"
                         f"\t\tиз них:\n"
                         f"\t\t\t\t- сыграно дома: {res_pars[10]}\n"
                         f"\t\t\t\t\t\t {res_pars[12]} - победы\n"
                         f"\t\t\t\t\t\t {res_pars[13]} - проигрыши\n"
                         f"\t\t\t\t\t\t {res_pars[14]} - ничьи\n"
                         f"Количество матчей гостей: {res_pars[9]}\n"
                         f"\t\tиз них:\n"
                         f"\t\t\t\t- сыграно в гостях: {res_pars[11]}\n"
                         f"\t\t\t\t\t\t {res_pars[15]} - победы\n"
                         f"\t\t\t\t\t\t {res_pars[16]} - проигрыши\n"
                         f"\t\t\t\t\t\t {res_pars[17]} - ничьи\n"
                         f"В личных встречах хозяева забили {res_pars[18]} и пропустили {res_pars[19]} мячей\n"
                         f"Чтобы начать заново введите команду /start",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.clear()