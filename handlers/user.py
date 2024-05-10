from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards import replykeyboards as reply

router = Router()

class Process(StatesGroup):
    name = State()
    number = State()
    question = State()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(text="Здравствуйте! Здесь вы можете отправить свой вопрос🤗", reply_markup=reply.rkb)


@router.message(F.text == "Регистрация")
async def reg(message: types.Message, state: FSMContext):
    await message.answer(text="Введите ваше имя:")
    await state.set_state(Process.name)


@router.message(Process.name)
async def set_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text="Введите ваш номер телефона:")
    await state.set_state(Process.number)


@router.message(Process.number)
async def set_number(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer(text="Задайте вопрос:")
    await state.set_state(Process.question)


@router.message(Process.question)
async def set_question(message: types.Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer(text="Спасибо за обращение, ваш вопрос обязательно будет рассмотрен!😋")