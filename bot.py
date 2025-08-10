import asyncio
from aiogram import Bot, Dispatcher
from handlers import controller
from sender import send_to_chat
import os
# Запуск бота
async def main(bot):
    dp = Dispatcher()

    dp.include_routers(controller.router)

    # Альтернативный вариант регистрации роутеров по одному на строку
    # dp.include_router(questions.router)
    # dp.include_router(different_types.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def bot_processes():
    bot = Bot(token=os.getenv('TG_TOKEN'))
    await asyncio.gather(main(bot), send_to_chat(bot))

if __name__ == "__main__":
    asyncio.run(bot_processes())