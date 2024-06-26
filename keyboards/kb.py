from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.requests import get_tickets


rkb = ReplyKeyboardMarkup(keyboard=
    [
        [
            KeyboardButton(text="✍ Регистрация")
        ]
    ],
    resize_keyboard=True
)

rkb_contact = ReplyKeyboardMarkup(keyboard=
    [
        [
            KeyboardButton(text="Отрпавить контакт", request_contact=True),
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)


ikb_newquestion = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Создать новый тикет", callback_data="new_ticket")
        ]
    ]
)


async def all_tickets():
    tickets = await get_tickets()
    keybaord = InlineKeyboardBuilder()
    for ticket in tickets:
        keybaord.add(InlineKeyboardButton(text=f"Тикет № {ticket.id}", callback_data=f"ticket_{ticket.id}"))
    return keybaord.adjust(2).as_markup()