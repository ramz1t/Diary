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
from Dairy.logic.key import add_new_student_key, get_student_keys, get_student_keys_for_export
from Dairy.logic.key import get_teacher_keys, get_teacher_keys_for_export, add_new_teacher_key
from Dairy.logic.school import check_school_in_db, add_new_school
from Dairy.logic.subject import add_new_subject
from Dairy.logic.teacher import create_new_teacher
from Dairy.models.admin import ChangePassword
from Dairy.models.group import ApiGroup
from Dairy.logic.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from Dairy.models.key import ApiKey, ApiTeacherKey
from Dairy.models.key import ApiKey
from Dairy.models.school import ApiSchool
from Dairy.models.subject import ApiSubject
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
    keys = get_student_keys(current_user.email)
    groups = get_groups(current_user.email)
    return templates.TemplateResponse('admin/panel.html', {"request": request,
                                                           "keys": keys,
                                                           "groups": groups,
                                                           "email": current_user.email})


@app.get('/student')
def studentprofile(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse('student/profile.html', {"request": request,
                                                               "email": current_user.email})


@app.post('/add_group_to_db')
def add_group(group: ApiGroup, current_user=Depends(get_current_user)):
    return add_new_group(group, current_user.email)


@app.post('/add_student_key_to_db')
def add_key(key: ApiKey, current_user=Depends(get_current_user)):
    return add_new_student_key(key, current_user.email)


@app.get('/admin/download/{filename}')
def download_file(filename, current_user=Depends(get_current_user)):
    create_file(filename, current_user.email)
    return FileResponse(f'./files/{filename}.txt',
                        media_type='application/octet-stream',
                        filename=filename)


@app.post("/change_user_password")
def change_password(body: ChangePassword, current_user=Depends(get_current_user)):
    return change_admin_password(email=current_user.email, old_password=body.old_password,
                                 new_password=body.new_password)


@app.get('/all_students/{group}')
def all_students(group):
    return get_all_students_from_group(group)


@app.get('/admin/manage_groups')
def manage_groups(request: Request, current_user=Depends(get_current_user)):
    groups = get_groups(current_user.email)
    return templates.TemplateResponse('admin/managegroups.html', {"request": request,
                                                                  "groups": sorted(groups)})


@app.get('/admin/add_student_key')
def add_key_page(request: Request, current_user=Depends(get_current_user)):
    groups = get_groups(current_user.email)
    keys = get_student_keys(current_user.email)
    return templates.TemplateResponse('admin/add_student_key.html', {"request": request,
                                                                     "groups": groups,
                                                                     "keys": keys})


@app.get('/admin/export_student_keys')
def export_page(request: Request, current_user=Depends(get_current_user)):
    keys_for_export = get_student_keys_for_export(current_user.email)
    return templates.TemplateResponse('admin/export_student_keys.html', {"request": request,
                                                                         "keys_for_export": keys_for_export})


@app.get('/admin/change_password')
def change_password_page(request: Request):
    return templates.TemplateResponse('admin/changepassword.html', {"request": request})


@app.get('/admin/add_group')
def add_group_page(request: Request, current_user=Depends(get_current_user)):
    groups = get_groups(current_user.email)
    return templates.TemplateResponse('admin/addgroup.html', {"request": request,
                                                              "groups": groups})


@app.get('/admin/add_teacher_key')
def add_key_page(request: Request, current_user=Depends(get_current_user)):
    keys = get_teacher_keys(current_user.email)
    return templates.TemplateResponse('admin/add_teacher_key.html', {"request": request,
                                                                     "keys": keys})


@app.get('/admin/export_teacher_keys')
def export_page(request: Request, current_user=Depends(get_current_user)):
    keys_for_export = get_teacher_keys_for_export(current_user.email)
    return templates.TemplateResponse('admin/export_teacher_keys.html', {"request": request,
                                                                         "keys_for_export": keys_for_export})


@app.post('/add_teacher_key_to_db')
def add_key(key: ApiTeacherKey, current_user=Depends(get_current_user)):
    return add_new_teacher_key(key, current_user.email)


@app.get('/admin/add_subject')
def add_subject_page(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse('admin/addsubject.html', {"request": request})


@app.post('/add_subject_to_db')
def add_subject(subject: ApiSubject):
    return add_new_subject(subject)


@app.get('/admin/school')
def school_page(request: Request, current_user=Depends(get_current_user)):
    availability = check_school_in_db(current_user.email)
    return templates.TemplateResponse('admin/school.html', {"request": request,
                                                            "number": current_user.email,
                                                            "availability": availability})


@app.post('/add_school_to_db')
def add_school(school: ApiSchool, current_user=Depends(get_current_user)):
    return add_new_school(school, school_id=current_user.email)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8003)
