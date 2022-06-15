from datetime import timedelta
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from Dairy.func.helpers import create_file
from Dairy.logic.admin import change_admin_password
from Dairy.logic.group import add_new_group, get_groups, get_all_students_from_group
from Dairy.logic.key import add_new_key, get_keys_by_school, get_keys_data_by_school
from Dairy.logic.teacher import create_new_teacher
from Dairy.models.admin import ChangePassword
from Dairy.models.group import ApiGroup
from Dairy.logic.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from Dairy.models.key import ApiKey
from Dairy.models.teacher import ApiTeacher
from Dairy.models.token import Token
from Dairy.models.student import ApiStudent
from Dairy.logic.student import create_new_student


app = FastAPI()
app.mount("/static", StaticFiles(directory="views/static"), name="static")
templates = Jinja2Templates(directory="views/templates")


@app.get('/')
def mainpage(request: Request):
    return templates.TemplateResponse('mainpage.html', {"request": request})


@app.get('/{usertype}/register')
def register(usertype: str, request: Request):
    return templates.TemplateResponse('register.html', {"request": request,
                                                        "usertype": usertype})


@app.post('/create_student')
def create_account(student: ApiStudent):
    response = create_new_student(student)
    return response


@app.post('/create_teacher')
def create_teacher(teacher: ApiTeacher):
    response = create_new_teacher(teacher)
    return response


@app.get('/{usertype}/login')
def login(usertype: str, request: Request):
    return templates.TemplateResponse('login.html', {"request": request,
                                                     "usertype": usertype})


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
        data={"sub": user.email, "type": usertype}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/admin')
def adminpage(request: Request, current_user=Depends(get_current_user)):
    keys = get_keys_by_school(current_user.email)
    groups = get_groups(current_user.email)
    return templates.TemplateResponse('admin/panel.html', {"request": request,
                                                           "keys": keys,
                                                           "groups": groups,
                                                           "email": current_user.email})


@app.get('/student')
def studentprofile(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse('student/profile.html', {"request": request,
                                                               "email": current_user.email})


@app.post('/add_group')
def add_group(group: ApiGroup, current_user=Depends(get_current_user)):
    return add_new_group(group, current_user.email)


@app.post('/add_key')
def add_key(key: ApiKey, current_user=Depends(get_current_user)):
    return add_new_key(key, current_user.email)


@app.get('/download/{filename}')
def download_file(filename, current_user=Depends(get_current_user)):
    create_file(filename, current_user.email)
    return FileResponse(f'./files/{filename}.txt',
                        media_type='application/octet-stream',
                        filename=filename)


@app.post("/change_password")
def change_password(body: ChangePassword, current_user=Depends(get_current_user)):
    return change_admin_password(email=current_user.email, old_password=body.old_password,
                                 new_password=body.new_password)


@app.get('/all_students/{group}')
def all_students(group):
    return get_all_students_from_group(group)


@app.get('/admin/managegroups')
def manage_groups(request: Request, current_user=Depends(get_current_user)):
    groups = get_groups(current_user.email)
    return templates.TemplateResponse('admin/managegroups.html', {"request": request,
                                                                  "groups": sorted(groups)})


@app.get('/admin/add_key')
def add_key_page(request: Request, current_user=Depends(get_current_user)):
    groups = get_groups(current_user.email)
    keys = get_keys_data_by_school(current_user.email)
    return templates.TemplateResponse('admin/addkey.html', {"request": request,
                                                            "groups": sorted(groups),
                                                            "keys": keys})


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8003)
