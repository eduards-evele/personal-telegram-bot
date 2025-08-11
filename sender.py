import openai
from aiogram import Bot, Dispatcher,types
import time
import os
import redis


async def get_openai_response(prompt):
    openai.api_key = os.getenv('OPENAI_TOKEN')
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

async def send_to_chat(bot):
    r = redis.Redis.from_url(os.getenv('REDIS_URL'))
    while True: #вечный цикл
        #получаем ответ от чата гпт
        quote = await get_openai_response(os.getenv('PROMPT'))
        #открываем список айди из файла
        if r.exists('subscribers'):
            subscribers = r.get('subscribers').decode('utf-8').split(';')
            for subscriber in subscribers:
                if subscriber != '':
                    await bot.send_message(chat_id=int(id), text=quote)
        time.sleep(60) #пауза 5 часов




