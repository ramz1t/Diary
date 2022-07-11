from datetime import timedelta
from typing import Union

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from Dairy.files.export import write_student_keys, write_teacher_keys
from Dairy.func.helpers import get_data_for_page\
    # , change_user_password, change_user_email
from Dairy.logic.cls import add_class_to_db
from Dairy.logic.group import add_new_group, get_all_students_from_group
from Dairy.logic.key import add_new_student_key
from Dairy.logic.key import add_new_teacher_key
from Dairy.logic.subject import add_new_subject
from Dairy.logic.teacher import create_new_teacher
# from Dairy.models.admin import ApiChangePassword, ApiChangeEmail
from Dairy.models.classes_rel import ApiClass
from Dairy.models.group import ApiGroup
from Dairy.logic.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from Dairy.models.key import ApiKey, ApiTeacherKey
from Dairy.models.subject import ApiSubject
from Dairy.models.teacher import ApiTeacher
from Dairy.models.token import Token
from Dairy.models.student import ApiStudent
from Dairy.crud_models import Adapter
from Dairy.crud_models import ApiBase

app = FastAPI()
app.mount("/static", StaticFiles(directory="views/static"), name="static")
templates = Jinja2Templates(directory="views/templates")
adapter = Adapter()


@app.post('/execute/{model}/{method}')
def execute(body: ApiBase, model: str, method: str):
    cls = adapter.clss[model]()
    func = getattr(cls, method)
    return func(body)



'''  login and register stuff  '''


@app.get('/')
def main_page(request: Request):
    return templates.TemplateResponse('mainpage.html', {"request": request})


@app.get('/{usertype}/register')
def register(usertype: str, request: Request):
    return templates.TemplateResponse('register.html', {"request": request,
                                                        "usertype": usertype})


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


''' pages '''


@app.get('/admin')
def admin_page(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse('admin.html', {"request": request})


@app.get('/student')
def student_profile(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse('student/profile.html', {"request": request,
                                                               "email": current_user.email})


@app.get('/teacher')
def teacher_profile(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse('teacher/profile.html', {"request": request,
                                                               "email": current_user.email})


@app.get('/load_page/{type}/{page}')
def load_page(type: str, page: str, request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(f'{type}/{page}.html',
                                      get_data_for_page(page=page, request=request, current_user=current_user))


''' DB urls'''


@app.post('/create_teacher')
def create_teacher(teacher: ApiTeacher, current_user=Depends(get_current_user)):
    response = create_new_teacher(teacher, current_user.email)
    return response


@app.post('/add_group_to_db')
def add_group(group: ApiGroup, current_user=Depends(get_current_user)):
    return add_new_group(group, current_user.email)


@app.post('/add_student_key_to_db')
def add_student_key(key: ApiKey, current_user=Depends(get_current_user)):
    return add_new_student_key(key, current_user.email)


@app.post('/add_teacher_key_to_db')
def add_teacher_key(key: ApiTeacherKey, current_user=Depends(get_current_user)):
    return add_new_teacher_key(key, current_user.email)


@app.post('/add_subject_to_db')
def add_subject(subject: ApiSubject, current_user=Depends(get_current_user)):
    return add_new_subject(subject, current_user.email)


# @app.post("/change_user_password")
# def change_password(body: ApiChangePassword, current_user=Depends(get_current_user)):
#     return change_user_password(email=current_user.email, body=body)
#
#
# @app.post('/change_user_email')
# def change_email(body: ApiChangeEmail):
#     return change_user_email(body=body)


@app.get('/all_students/{group}')
def all_students(group):
    return get_all_students_from_group(group)


@app.post('/add_class_to_db')
def add_class(body: ApiClass, current_user=Depends(get_current_user)):
    return add_class_to_db(body, current_user.email)


''' download urls'''


@app.get('/download_group/{groupname}')
def download_file(groupname, current_user=Depends(get_current_user)):
    write_student_keys(groupname, current_user.email)
    return FileResponse(f'./files/{groupname}.txt',
                        media_type='application/octet-stream',
                        filename=groupname)


@app.get('/download_teachers')
def download_teachers(current_user=Depends(get_current_user)):
    write_teacher_keys(current_user.email)
    return FileResponse(f'./files/teachers.txt',
                        media_type='application/octet-stream',
                        filename='teachers')


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8003)
