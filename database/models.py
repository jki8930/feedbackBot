from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, sessionmaker
from sqlalchemy.types import BigInteger, String
from sqlalchemy import ForeignKey

engine = create_async_engine(url="", echo=False)

async_session = sessionmaker(engine)

class Base(DeclarativeBase):
    ...

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger())
    name: Mapped[str] = mapped_column(String(30))
    number: Mapped[str] = mapped_column(String(15))


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("users.tg_id"))
    question: Mapped[str] = mapped_column(String(1000))