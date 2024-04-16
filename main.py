import os
import asyncio
from handlers import router
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from models import async_main


async def main():
    await async_main()

    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[INFO] Exit...")
