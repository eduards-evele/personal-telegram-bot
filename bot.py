import asyncio
from aiogram import Bot, Dispatcher
from handlers import controller
from sender import send_to_chat
from aiogram.fsm.storage.redis import RedisStorage, Redis
import os

async def main(bot):
    redis = Redis.from_url(os.getenv('REDIS_URL'))  

    storage = RedisStorage(redis=redis)
    dp = Dispatcher(storage=storage)

    dp.include_routers(controller.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def bot_processes():
    bot = Bot(token=os.getenv('TG_TOKEN'))
    await asyncio.gather(main(bot), send_to_chat(bot))

if __name__ == "__main__":
    asyncio.run(bot_processes())