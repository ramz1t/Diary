from datetime import timedelta
from tokenize import group
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse, RedirectResponse

from files.export import write_student_keys, write_teacher_keys
from func.helpers import check_date, make_dates_for_week, get_title, teaching_days_dates, set_permissions
from logic.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user, \
    validate_token
from models.token import Token
from crud_models import CRUDAdapter
from crud_models import ApiBase
from pages import PagesAdapter, ApiPage


#don't forget to set debug=False on production server!!!
app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="views/static"), name="static")
templates = Jinja2Templates(directory="views/templates")
crudadapter = CRUDAdapter()
pagesadapter = PagesAdapter()


@app.post('/execute/{model}/{method}')
def execute(body: ApiBase, model: str, method: str):
    cls = crudadapter.clss[model]()
    func = getattr(cls, method)
    return func(body)


'''  login and register stuff  '''


@app.get('/')
def main_page(request: Request):
    token_valid, type = validate_token(request.cookies.get('access_token'))
    if token_valid:
        return RedirectResponse(f'/{type}')
    return templates.TemplateResponse('mainpage.html', {"request": request})


@app.get('/{usertype}/register')
def register(usertype: str, request: Request):
    return templates.TemplateResponse('register.html', {"request": request,
                                                        "usertype": usertype})


@app.get('/{usertype}/login')
def login(usertype: str, request: Request):
    return templates.TemplateResponse('login.html', {"request": request,
                                                     "usertype": usertype})


@app.post("/token", response_model=Token)
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(email=form_data.username, password=form_data.password, type=form_data.client_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    REMEMBER_ME = form_data.client_secret
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES if REMEMBER_ME == 'false' else 365 * 24 * 60)
    access_token = create_access_token(
        data={"sub": user.email, "type": form_data.client_id}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=False)
    return {"access_token": access_token, "token_type": "bearer"}


''' pages '''


@app.get('/admin')
def admin_page(request: Request, current_user=Depends(get_current_user)):
    if current_user.__tablename__ != 'admins':
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content='no access with this usertype')
    return templates.TemplateResponse('admin.html', {"request": request,
                                                     "link": crudadapter.clss['admin']().check_link(current_user.id),
                                                     "user_id": current_user.id})


@app.get('/student')
def student_profile(request: Request, current_user=Depends(get_current_user)):
    if current_user.__tablename__ != 'students':
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content='no access with this usertype')
    return templates.TemplateResponse('student.html', {"request": request,
                                                       "user_id": current_user.id})


@app.get('/teacher')
def teacher_profile(request: Request, current_user=Depends(get_current_user)):
    if current_user.__tablename__ != 'teachers':
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content='no access with this usertype')
    return templates.TemplateResponse('teacher.html', {"request": request,
                                                       "user_id": current_user.id})


@app.patch('/load_page/')
def load_page(body: ApiPage, page: str, type: str, request: Request, current_user=Depends(get_current_user)):
    try:
        return pagesadapter.pages[page]().export(body=body, request=request, current_user=current_user)
    except KeyError:
        return templates.TemplateResponse(f'{type}/{page}.html', {'request': request})


@app.post('/add_lesson')
def add_lesson(body: ApiPage, request: Request):
    classes = crudadapter.clss['cls']().for_schedule(body)
    print(classes)
    return templates.TemplateResponse('admin/class.html', {"request": request,
                                                           "day_i": body.day_i,
                                                           "lesson_i": body.lesson_i + 1,
                                                           "classes": classes})


@app.post('/search_school')
def search_school(body: ApiBase, request: Request):
    data = crudadapter.clss['school']().find(body)
    return templates.TemplateResponse('admin/school_card.html', {"request": request, "school_data": data, })


@app.patch('/load_schedule')
def load_schedule(body: ApiBase, group_id: int, request: Request):
    days_titles = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    classes = crudadapter.clss['cls']().for_schedule(body)
    data = crudadapter.clss['scheduleclass']().get_schedule(group_id)
    return templates.TemplateResponse('admin/schedule.html', {"request": request, "data": data, "classes": classes,
                                                              "days": days_titles})


@app.get('/load_teacher_classes')
def load_teacher_classes(teacher_id: int):
    return crudadapter.clss['cls'].for_teacher(teacher_id)


@app.post('/upgrade_groups')
def upgrade_groups(body: ApiBase):
    return crudadapter.clss['group']().upgrade(body)


@app.post('/{model}/delete')
def delete_from_db(id: int, model: str):
    return crudadapter.clss[model].delete(id)


''' DB urls'''

# @app.post("/change_user_password")
# def change_password(body: ApiChangePassword, current_user=Depends(get_current_user)):
#     return change_user_password(email=current_user.email, body=body)
#
#
# @app.post('/change_user_email')
# def change_email(body: ApiChangeEmail):
#     return change_user_email(body=body)


''' download urls'''


@app.get('/download_group/{groupname}')
def download_file(groupname, current_user=Depends(get_current_user)):
    write_student_keys(groupname, current_user.id)
    return FileResponse(f'./files/{groupname}.txt',
                        media_type='application/octet-stream',
                        filename=f'{groupname}.txt')


@app.get('/download_teachers')
def download_teachers(current_user=Depends(get_current_user)):
    write_teacher_keys(current_user.id)
    return FileResponse(f'./files/teachers.txt',
                        media_type='application/octet-stream',
                        filename='teachers.txt')


@app.get('/weather_photo')
def get_weather_photo(weather: str):
    return FileResponse(f'./views/static/photos/weather/{weather}.jpg')


@app.get('/load_diary')
def load_diary(date: str, current_user=Depends(get_current_user)):
    return crudadapter.clss['book'].make_day(date, current_user)


@app.get('/get_dates_for_next_week')
def get_dates(date: str, type: str):
    return make_dates_for_week(date, type=type)


@app.get('/class_book')
def class_book(group_id: int, class_id: int):
    return crudadapter.clss['book'].make_class(group_id, class_id)


@app.post('/edit_tg_permissions')
def edit_tg_permissions(hw: bool, mark: bool, current_user=Depends(get_current_user)):
    return set_permissions(hw, mark, current_user.id)


@app.get('/final_marks')
def get_final_marks_for_table(class_id: int):
    return crudadapter.clss['book'].get_final(class_id)


@app.get('/class_homework')
def get_class_homework(group_id: int):
    return {'hw': crudadapter.clss['homework'].group_hw(group_id), 
    'dates': crudadapter.clss['scheduleclass'].get_eight_teacher_working_days(group_id)}


@app.get('/download_privacy')
def download_privacy():
    return FileResponse(f'./files/Privacy.pdf',
                        media_type='application/octet-stream',
                        filename='Privacy.pdf')


if __name__ == '__main__':
    uvicorn.run("__main__:app", host='127.0.0.1', port=8000, reload=True)
