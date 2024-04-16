from models import async_session
from models import Student, Discipline, Rating
from sqlalchemy import select


async def get_disciplines():
    async with async_session() as session:
        return await session.scalars(select(Discipline))


async def get_students():
    async with async_session() as session:
        return await session.scalars(select(Student))


async def get_titles(discipline_id, student_id):
    async with async_session() as session:
        discipline = await session.scalar(select(Discipline).where(Discipline.id == int(discipline_id)))
        student = await session.scalar(select(Student).where(Student.id == int(student_id)))

        return discipline.discipline_name, student.student_name


async def get_rating(discipline, student):
    async with async_session() as session:
        return await session.scalar(select(Rating).where(Rating.discipline == int(discipline)).where(
            Rating.student == int(student)))
