from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import openai
from redis import asyncio as redis
import os
from aiogram.fsm.context import FSMContext
from handlers.user_states import UserStates
from datetime import datetime

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state : FSMContext):
    r = redis.from_url(os.getenv('REDIS_URL'))
    await state.set_state(UserStates.choosing_frequency)

    chat_id = message.chat.id 
    if not await r.exists('subscribers'):
        await r.set('subscribers', str(chat_id))
    else:
        ids_str = await r.get('subscribers').decode('utf-8')
        ids = ids_str.split(';')
        if str(chat_id) not in ids:
            ids_str += f';{chat_id}'
            await r.set('subscribers', ids_str)
  
    await message.answer("Введите частоту получения цитаты в минутах")


@router.message(Command("about"))
async def cmd_about(message: Message, state : FSMContext):
    
    data = await state.get_data()
    frequency = data.get('frequency')
    await message.answer(f'Частота получения цитат: {frequency}')

@router.message(Command("reset"))
async def cmd_reset(message: Message, state : FSMContext):
    await state.clear()
    r = redis.from_url(os.getenv('REDIS_URL'))
    if await r.exists('subscribers'):
        chat_id = str(message.chat.id)
        subscribers = await r.get('subscribers').decode('utf-8').split(';')
        subscribers.remove(chat_id)
        s = ''
        for x in subscribers:
            s += f'{x};'
        await r.set('subscribers', s)
    await message.answer("Бот сброшен. Нажмите /start для перезапуска")

@router.message(Command("change"), UserStates.receiving_quotes)
async def cmd_change(message : Message, state: FSMContext):
    await state.set_state(UserStates.choosing_frequency)
    await message.answer("Введите новую частоту получения цитаты: ")


@router.message(UserStates.choosing_frequency, F.text)
async def cmd_choose_frequency(message : Message, state: FSMContext):
    try:
        frequency = float(message.text)
        await state.update_data(frequency=frequency)
        await state.set_state(UserStates.receiving_quotes)
        now = datetime.now()
        await state.update_data(msg_time=now.strftime("%m/%d/%Y, %H:%M:%S"))
        await message.answer(f'Вы будете получать цитату раз в {frequency} мин.')
    
    except ValueError:
        await message.answer("Введите частоту в минутах")
