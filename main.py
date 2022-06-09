from datetime import timedelta

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm

from Dairy.logic.group import add_new_group
from Dairy.models.group import ApiGroup
from Dairy.logic.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from Dairy.models.token import Token
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run


app = FastAPI()
app.mount("/static", StaticFiles(directory="views/static"), name="static")
templates = Jinja2Templates(directory="views/templates")


@app.get('/')
def mainpage(request: Request):
    return templates.TemplateResponse('mainpage.html', {"request": request})


@app.get('/register')
def register(request: Request):
    return templates.TemplateResponse('register.html', {"request": request})


@app.get('/login')
def login(request: Request):
    return templates.TemplateResponse('login.html', {"request": request})


@app.post("/token/{usertype}", response_model=Token)
def login_for_access_token(usertype, response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(email=form_data.username, password=form_data.password, type=usertype)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/admin')
def adminpage(request: Request):
    return templates.TemplateResponse('admin/panel.html', {"request": request})


@app.get('/groups')
def groups():
    pass


@app.post('/add_group')
def add_group(group: ApiGroup):
    return add_new_group(group)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001)
