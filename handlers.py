from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from requests import get_rating, get_titles
import keyboards as kb

router = Router()


class Initialization(StatesGroup):
    discipline = State()
    student = State()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    await state.set_state(Initialization.discipline)
    await message.answer(f"Здравствуйте, {message.from_user.full_name}!\n"
                         "Я ваш помощник по посещаемости и баллам за дисциплины.")
    await message.answer(f"Выберите дисциплину: ", reply_markup=await kb.inline_disciplines())


@router.callback_query(F.data == 'to_main')
async def main_board(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Initialization.discipline)
    await callback.message.edit_text(f"Выберите дисциплину: ", reply_markup=await kb.inline_disciplines())


@router.callback_query(Initialization.discipline)
async def disciplines(callback: CallbackQuery, state: FSMContext):
    await state.update_data(discipline=callback.data)
    await callback.answer("Вы выбрали дисциплину!")
    await state.set_state(Initialization.student)
    await callback.message.edit_text("Выберите студента из списка ниже: ", reply_markup=await kb.inline_students())


@router.callback_query(Initialization.student)
async def students(callback: CallbackQuery, state: FSMContext):
    await state.update_data(student=callback.data)
    await callback.answer("Вы выбрали студента!")
    data = await state.get_data()

    try:
        rating = await get_rating(data['discipline'].split('_')[1], data['student'].split('_')[1])
        titles = await get_titles(data['discipline'].split('_')[1], data['student'].split('_')[1])

        await callback.message.edit_text(f"📊 Дисциплина: {titles[0]}\n"
                                         f"👤 Студент: {titles[1]}\n"
                                         f"✔ Посещение: {rating.attendance}%\n"
                                         f"💯 Баллы за дисциплину: {rating.score}/100", reply_markup=kb.main_kb)
    except AttributeError:
        await callback.message.edit_text("Произошла ошибка...", reply_markup=kb.main_kb)

    await state.clear()


@router.message()
async def command_start_handler(message: Message):
    await message.answer(f"Я вас не понимаю... 😔\n"
                         f'Нажмите кнопку "На главную" или напишите /start', reply_markup=kb.main_kb)
