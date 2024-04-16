import os
from dotenv import load_dotenv
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

load_dotenv()
engine = create_async_engine(url=os.getenv('DB_URL'))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(primary_key=True)
    student_name: Mapped[str] = mapped_column(String(255))


class Discipline(Base):
    __tablename__ = 'disciplines'

    id: Mapped[int] = mapped_column(primary_key=True)
    discipline_name: Mapped[str] = mapped_column(String(100))


class Rating(Base):
    __tablename__ = 'ratings'

    id: Mapped[int] = mapped_column(primary_key=True)
    student: Mapped[int] = mapped_column(ForeignKey('students.id'))
    discipline: Mapped[int] = mapped_column(ForeignKey('disciplines.id'))
    score: Mapped[int] = mapped_column()
    attendance: Mapped[int] = mapped_column()


async def async_main():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
