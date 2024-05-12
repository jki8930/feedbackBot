from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards import replykeyboards as reply
from database import requests as rq


router = Router()

class Process(StatesGroup):
    name = State()
    number = State()
    question = State()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(text="Здравствуйте! Здесь вы можете отправить свой вопрос 🤗", reply_markup=reply.rkb)


@router.message(F.text == "✍ Регистрация")
async def reg(message: types.Message, state: FSMContext):
    await message.answer(text="Введите ваше имя")
    await state.set_state(Process.name)


@router.message(Process.name)
async def set_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text="Нажмите кнопку, чтобы дать нам номер Вашего телефона для обратной связи", reply_markup=reply.rkb_contact)
    await state.set_state(Process.number)
    await rq.add_user(message.from_user.id)


@router.message(F.text == "Назад")
async def to_back(message: types.Message):
    await message.answer(text="Здравствуйте! Здесь вы можете отправить свой вопрос 🤗", reply_markup=reply.rkb)


@router.message(Process.number)
async def set_number(message: types.Message, state: FSMContext):
    if message.contact:
        await state.update_data(number=int(message.contact.phone_number[1:]))
        await message.answer(text="Задайте вопрос")
        await state.set_state(Process.question)
    else:
        await message.answer("Вы не сможете задать вопрос, пока не дадите нам ваши контакты 😫", reply_markup=reply.rkb_contact)
        await state.clear()


@router.message(Process.question)
async def set_question(message: types.Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer(text="Спасибо за обращение, ваш вопрос обязательно будет рассмотрен! 😋")
    await state.clear()