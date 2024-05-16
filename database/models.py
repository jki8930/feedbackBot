from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.types import BigInteger, String
from sqlalchemy import ForeignKey

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3", echo=False)

async_session = async_sessionmaker(engine)

class Base(DeclarativeBase):
    ...

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger())
    name: Mapped[str] = mapped_column(String(30), nullable=True)
    number: Mapped[str] = mapped_column(String(15), nullable=True)
    username: Mapped[str] = mapped_column(String(30), nullable=True)

class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    user = mapped_column(ForeignKey("users.id"))
    question: Mapped[str] = mapped_column(String(1000))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)