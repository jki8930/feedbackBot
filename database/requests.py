from .models import User, Ticket, async_session
from sqlalchemy import select, update, delete
from typing import Any

async def add_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
            return False
        elif user.name:
            return True
        return False


async def edit_user(tg_id, name, number, username: str | Any | None):
    async with async_session() as session:
        user = await session.execute(update(User).where(User.tg_id == tg_id).values(
            name=name, 
            number=number, 
            username=username
        ))
        await session.commit()


async def add_ticket(tg_id, question):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        session.add(Ticket(user=user.id, question=question))
        await session.commit()


async def get_tickets():
    async with async_session() as session:
        tickets = await session.scalars(select(Ticket))
        return tickets