import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from src.conifg import REDIS_PORT, TOKEN
from src import handlers, callbacks

logging.basicConfig(level=logging.INFO)
storage = RedisStorage.from_url(f'redis://localhost:{REDIS_PORT}/0')
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

dp.include_routers(handlers.router)
dp.include_routers(callbacks.router)

user = 'Иванов Иван'


# Запуск процесса поллинга новых апдейтов
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())