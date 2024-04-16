from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from requests import get_disciplines, get_students

main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='На главную 🔙', callback_data='to_main')]
])


async def inline_disciplines():
    disciplines = await get_disciplines()
    keyboard = InlineKeyboardBuilder()

    for discipline in disciplines:
        keyboard.add(InlineKeyboardButton(text=discipline.discipline_name, callback_data=f'discipline_{discipline.id}'))

    return keyboard.adjust(1).as_markup()


async def inline_students():
    students = await get_students()
    keyboard = InlineKeyboardBuilder()

    for student in students:
        keyboard.add(InlineKeyboardButton(text=student.student_name, callback_data=f'student_{student.id}'))
    keyboard.add(InlineKeyboardButton(text='На главную 🔙', callback_data='to_main'))

    return keyboard.adjust(1).as_markup()
