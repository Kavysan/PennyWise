from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from typing import List


class ExpenseTable(Base):
    __tablename__ = "expense_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    expense_item: Mapped[str] = mapped_column(String(120))
    cost: Mapped[float] = mapped_column(Float(10))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    user: Mapped["UserTable"] = relationship(back_populates="expenses")

    def __repr__(self) -> str:
        return f"ExpenseTable (id={self.id!r}, expense item={self.expense_item!r}, cost={self.cost!r})"
    
class UserTable(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(50))
    expenses: Mapped[List["ExpenseTable"]] = relationship(back_populates="user")
