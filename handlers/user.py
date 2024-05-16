from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards import kb as reply
from database import requests as rq
from aiogram.types import ReplyKeyboardRemove


router = Router()

class Process(StatesGroup):
    name = State()
    number = State()
    question = State()


@router.message(CommandStart())
async def start(message: types.Message):
    user = await rq.add_user(message.from_user.id)
    if not user:
        await message.answer(text="Здравствуйте! Здесь вы можете отправить свой вопрос 🤗", 
        reply_markup=reply.rkb)
    else:
        await message.answer(text="Отпарвить новый запрос можно по кнопке ниже")


@router.message(F.text == "✍ Регистрация")
async def reg(message: types.Message, state: FSMContext):
    await message.answer(text="Введите ваше имя", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Process.name)


@router.message(Process.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text="Нажмите кнопку, чтобы дать нам номер Вашего телефона для обратной связи", 
    reply_markup=reply.rkb_contact)
    await state.set_state(Process.number)


@router.message(F.text == "Назад")
async def to_back(message: types.Message):
    await message.answer(text="Здравствуйте! Здесь вы можете отправить свой вопрос 🤗", 
    reply_markup=reply.rkb)


@router.message(Process.number, F.contact)
async def get_number(message: types.Message, state: FSMContext):
    await state.update_data(number=int(message.contact.phone_number[1:]))
    await message.answer(text="Задайте вопрос", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Process.question)


@router.message(Process.question)
async def get_question(message: types.Message, state: FSMContext):
    user = await state.get_data()
    await rq.edit_user(message.from_user.id, user['name'], user['number'], message.from_user.username)
    await rq.add_ticket(message.from_user.id, message.text)
    await message.answer("Ваше обращение будет рассмотрено, спасибо ☺")
    await state.clear()