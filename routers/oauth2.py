from fastapi import Depends, HTTPException, status, Cookie, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
from routers.tokens import verify_token 
# from fastapi.security import OAuth2PasswordBearer
from database import get_db
import models
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     return verify_token(token,credentials_exception)

async def get_current_user(
    access_token: str | None = Cookie(None),
    db: Session = Depends(get_db)
):
    if not access_token:
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        return None
    
    if access_token.startswith("Bearer "):
        access_token = access_token[7:]
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token_data = verify_token(access_token, credentials_exception)
    
    # Get actual user from DB
    user = db.query(models.UserTable).filter(models.UserTable.email == token_data.username).first()
    if not user:
        raise credentials_exception
        # return None
    return user
    

def require_user(request: Request, user: models.UserTable = Depends(get_current_user)):
    if user is None:
        return templates.TemplateResponse("signin.html", {"request": request, "error": "Login to view expenses"})
    return user