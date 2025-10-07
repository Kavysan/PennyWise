from fastapi import APIRouter, Depends, status, HTTPException, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
import schemas
import models
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from routers.oauth2 import require_user, get_current_user
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

router = APIRouter(
    tags=['expense'],
    prefix='/expense'
    )


@router.post("/add", status_code=201)
def create_expense_form(
    expense_item: str = Form(...),
    cost: float = Form(...),
    db: Session = Depends(get_db),
    current_user: models.UserTable = Depends(require_user)
):
    new_expense = models.ExpenseTable(
        expense_item=expense_item,
        cost=cost,
        user_id=current_user.id
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return RedirectResponse(url="/expense", status_code=303)


# @router.get("/", response_class=HTMLResponse)
# def get_all_expenses(
#     request: Request,
#     db: Session = Depends(get_db),
#     current_user: models.UserTable = Depends(require_user)
# ):
#     expenses = db.query(models.ExpenseTable).filter(models.ExpenseTable.user_id == current_user.id).all()
#     return templates.TemplateResponse(
#         "expense.html",
#         {"request": request, "expenses": expenses, "user": current_user}
#     )

@router.get("/", response_class=HTMLResponse)
def get_all_expenses(request: Request, db: Session = Depends(get_db), current_user: models.UserTable | None = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse("/login") 
    expenses = db.query(models.ExpenseTable).filter(models.ExpenseTable.user_id == current_user.id).all()
    return templates.TemplateResponse("expense.html", {"request": request, "expenses": expenses, "user": current_user})


# @router.get('/{id}', response_model=schemas.ShowExpense, status_code=status.HTTP_202_ACCEPTED)
# def get_expense(id: int, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(require_user)):
#     expense = db.query(models.ExpenseTable).filter(models.ExpenseTable.id == id).first()
#     if not expense:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This is not a valid id")
#     return expense

@router.get("/edit/{id}", response_class=HTMLResponse)
def edit_expense_page(
    id: int, 
    request: Request, 
    db: Session = Depends(get_db), 
    current_user: models.UserTable = Depends(require_user)
    ):
    if not current_user:
        return RedirectResponse("/login") 
    expense = db.query(models.ExpenseTable).filter(models.ExpenseTable.id == id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    return templates.TemplateResponse(
        "edit_expense.html",
        {"request": request, "expense": expense, "user": current_user}
    )

@router.post("/edit/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_expense_form(
    id: int,
    expense_item: str = Form(...),
    cost: float = Form(...),
    db: Session = Depends(get_db),
    current_user: models.UserTable = Depends(require_user)
):
    if not current_user:
        return RedirectResponse("/login") 
    expense = db.query(models.ExpenseTable).filter(models.ExpenseTable.id == id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Invalid expense ID")

    expense.expense_item = expense_item
    expense.cost = cost
    db.commit()
    db.refresh(expense)

    return RedirectResponse(url="/expense", status_code=303)


# @router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
# def update_expense(request: schemas.AddExpense, id: int, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(require_user)):
#     expense = db.query(models.ExpenseTable).filter(models.ExpenseTable.id == id)
#     if not expense.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This is not a valid id")
#     expense.update(request.model_dump(), synchronize_session=False)
#     db.commit()
#     return {"detail":"updated successfully"}


@router.post('/delete/{id}', status_code=status.HTTP_202_ACCEPTED)
def delete_expense(id: int, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(require_user)):
    if not current_user:
        return RedirectResponse("/login") 
    
    expense = db.query(models.ExpenseTable).filter(models.ExpenseTable.id == id)
    if not expense.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not a valid id")
    expense.delete(synchronize_session=False)
    db.commit()
    return RedirectResponse(url="/expense", status_code=303)
