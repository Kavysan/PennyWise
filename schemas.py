from pydantic import BaseModel
from typing import List

#--------------- input schemas ------------#
class AddExpense(BaseModel):
    expense_item: str
    cost: float
    user_id: int

class AddUser(BaseModel):
    name: str
    email: str
    password: str

#----------------- output schemas ----------#
class ShowExpense(BaseModel):
    id: int
    expense_item: str
    cost: float
    user_id: int

    class Config:
        from_attributes = True

class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    password: str
    expenses: List[ShowExpense] = []

    class Config:
        from_attributes = True

#------------ Authentication Schema ----------#

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None