from openai import AsyncOpenAI
from aiogram import Bot, Dispatcher,types
from aiogram.filters import Command
import time
import os
from redis import asyncio as redis
import asyncio
from datetime import datetime, timedelta
import json
async def get_openai_response(prompt):
    print(os.getenv('TG_TOKEN'))
    client = AsyncOpenAI(api_key=os.getenv('OPENAI_TOKEN'))
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

async def send_to_chat(bot):
    r = redis.from_url(os.getenv('REDIS_URL'))
    while True: 
        now = datetime.now()

       

        if await r.exists('subscribers'):
            subscribers = await r.get('subscribers')
            subscribers = subscribers.decode('utf-8').split(';')
            for subscriber in subscribers:
                if subscriber != '':
                    key_ = f'fsm:{subscriber}:{subscriber}:data'
                    exists_ = await r.exists(key_)
                    if exists_:
                        try:
                            raw = await r.get(key_)
                            raw = raw.decode('utf-8')
                            data = json.loads(raw)
                            frequency = float(data['frequency'])
                            msg_time = datetime.strptime(data['msg_time'], "%m/%d/%Y, %H:%M:%S")

                            if now >= msg_time + timedelta(seconds=frequency*60):
                                print('qqq')
                                asyncio.create_task(send_msg(bot, subscriber))
                                data['msg_time'] = now.strftime("%m/%d/%Y, %H:%M:%S")
                                
                                await r.set(key_, json.dumps(data))
                        except Exception:
                            pass
        await asyncio.sleep(1)

async def send_msg(bot : Bot, chat_id : str):
    print('aaa')
    quote = await get_openai_response(os.getenv('PROMPT'))
    await bot.send_message(chat_id=int(chat_id), text=quote)


