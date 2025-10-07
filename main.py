from fastapi import FastAPI, Request
from routers import expense, user, authentication
import models
from database import engine
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import RedirectResponse

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home_page(request: Request):
    return RedirectResponse(url="/expense")

app.include_router(expense.router)
app.include_router(user.router)
app.include_router(authentication.router)