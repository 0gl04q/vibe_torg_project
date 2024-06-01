import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from handlers import menu, create_order, list_order, maintenance
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO,
                    # filename="log/service.log",
                    # filemode="a",
                    format="%(asctime)s %(name)s %(levelname)s %(message)s")

bot = Bot(token=os.getenv('BOT_TOKEN'))


async def main():
    dp = Dispatcher(storage=MemoryStorage(), maintenance_mode=False)

    dp.include_routers(menu.router,  create_order.router, list_order.router, maintenance.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
