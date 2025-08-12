import openai
from aiogram import Bot, Dispatcher,types
from aiogram.filters import Command
import time
import os
import redis
import asyncio
from datetime import datetime, timedelta
import json
async def get_openai_response(prompt):
    openai.api_key = os.getenv('OPENAI_TOKEN')
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

async def send_to_chat(bot):
    r = redis.Redis.from_url(os.getenv('REDIS_URL'))
    while True: 
        now = datetime.now()

       

        if r.exists('subscribers'):
            subscribers = r.get('subscribers').decode('utf-8').split(';')
            for subscriber in subscribers:
                if subscriber != '':
                    key_ = f'fsm:{subscriber}:{subscriber}:data'
                    
                    if r.exists(key_):
                        try:
                            data = json.loads(r.get(key_).decode('utf-8'))
                            frequency = float(data['frequency'])
                            msg_time = datetime.strptime(data['msg_time'], "%m/%d/%Y, %H:%M:%S")

                            if now >= msg_time + timedelta(seconds=frequency*60):
                                asyncio.create_task(send_msg(str(message.chat.id)))
                                data['msg_time'] = now.strftime("%m/%d/%Y, %H:%M:%S")
                                
                                r.set(key_, json.dumps(data))
                        except Exception:
                            pass
        await asyncio.sleep(1)

async def send_msg(chat_id : str):
    quote = await get_openai_response(os.getenv('PROMPT'))
    await bot.send_message(chat_id=int(subscriber), text=quote)


