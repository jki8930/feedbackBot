import os
from dotenv import load_dotenv
from aiogram import Router, types
from aiogram.filters import BaseFilter, Command
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards.kb import all_tickets

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


# @router.callback_query(F.data.startswith('ticket_'))
# async def answer_ticket(callback: CallbackQuery, state: FSMContext):
#     await state.set_state(Answer.answer)
#     await callback.answer('Вы выбрали тикет')