from fastapi import Depends, Form, status, APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import models
from sqlalchemy.orm import Session
from database import get_db
import hashing 
from routers import tokens
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

router = APIRouter(
    tags=['authentication']
)

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str | None = None):
    message = "Please log in to view expenses" if error == "login_required" else None
    return templates.TemplateResponse("signin.html", {"request": request, "error": message})
    # return templates.TemplateResponse("signin.html", {"request": request})

@router.post("/login")
async def login_user(request: Request,
                     username: str = Form(...),
                     password: str = Form(...),
                     db: Session = Depends(get_db)):
    user = db.query(models.UserTable).filter(models.UserTable.email == username).first()

    if not user :
        # Invalid login -> render login page with error
        return templates.TemplateResponse("signin.html", {"request": request, "error": "Invalid username, please try again!"})
    
    if not hashing.verify_password(password, user.password):
        return templates.TemplateResponse("signin.html", {"request": request, "error": "Invalid password, please try again!"})
    
    access_token = tokens.create_access_token(data={"sub": user.email})
    response = RedirectResponse(url="/expense", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        path="/"  # ensures cookie is sent on all routes
    )
    return response

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
async def signup_user(
    request: Request, 
    name: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    password_repeat: str = Form(...),
    db: Session = Depends(get_db)
):

    existing_user = db.query(models.UserTable).filter(models.UserTable.email == username).first()
    if existing_user:
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": "User already exists, Please Login."}
        )

    # Check if passwords match
    if password != password_repeat:
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": "Passwords do not match"}
        )

    # Create new user
    new_user = models.UserTable(
        name = name,
        email=username,
        password=hashing.get_password_hash(password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="access_token", path="/")  # must match path="/"
    return response