from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column,DeclarativeBase,Mapped,relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)

    address: Mapped[list["Address"]] = relationship(back_populates="user")

class Address(Base):
    __tablename__ = 'addresses'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates="address")