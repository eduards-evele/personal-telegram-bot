from aiogram import Router, F
from aiogram.types import Message
import openai
import redis
import os
router = Router()

@router.message(F.text) #функция, которая срабатывает на все текстовые сообщения
async def message_with_text(message: Message):  #объект сообщения, содержащий все данные о нем
    r = redis.Redis.from_url(os.getenv('REDIS_URL'))
    chat_id = message.chat.id #получение айди чата с пользователем
    if not r.exists('subscribers'):
        r.set('subscribers', str(chat_id))
    else:
        ids_str = r.get('subscribers')
        ids = ids_str.split(';')
        if chat_id not in ids:
            ids_str += f';{chat_id}'
            r.set('subscribers', ids_str)
    await message.answer(f'your id: {str(chat_id)}') #отправить ответ пользователю


