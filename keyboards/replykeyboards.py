from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


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