import os
from dotenv import load_dotenv
from aiogram import Router, types, F
from aiogram.filters import BaseFilter, Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards.kb import all_tickets
from database import requests as rq

router = Router()


class Answer(StatesGroup):
    answer = State()


class CheckAdmin(BaseFilter):
    def __init__(self):
        self.admins = [1339062105]

    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in self.admins


@router.message(CheckAdmin(), Command('tickets'))
async def tickets(message: types.Message):
    await message.answer("Список тикетов:", reply_markup=await all_tickets())


@router.callback_query(F.data.startswith('ticket_'))
async def answer_ticket(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Answer.answer)
    await callback.answer('Вы выбрали тикет')
    ticket = await rq.get_ticket(callback.data.split("_")[1])
    user = await rq.get_user(ticket.user)
    await callback.message.answer(f"Вопрос: {ticket.question}\n\n{user.name} | {user.username} | {user.number}\n\nНапишите ответ")


@router.message(Answer.answer)
async def set_answer(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)