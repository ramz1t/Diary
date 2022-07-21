from datetime import timedelta
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse

from Dairy.files.export import write_student_keys, write_teacher_keys
from Dairy.logic.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from Dairy.models.day import AddLesson
from Dairy.models.token import Token
from Dairy.crud_models import CRUDAdapter
from Dairy.crud_models import ApiBase
from Dairy.pages import PagesAdapter, ApiPage

app = FastAPI()
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
    return templates.TemplateResponse('teacher/profile.html', {"request": request,
                                                               "user_id": current_user.id})


@app.patch('/load_page/')
def load_page(body: ApiPage, request: Request):
    try:
        return pagesadapter.pages[body.page]().export(body=body, request=request)
    except KeyError:
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', {'request': request})


@app.post('/add_lesson')
def add_lesson(body: ApiPage, request: Request):
    classes = crudadapter.clss['cls']().get(body)
    return templates.TemplateResponse('admin/class.html', {"request": request,
                                                           "day_i": body.day_i,
                                                           "lesson_i": body.lesson_i + 1,
                                                           "classes": classes})


@app.post('/search_school')
def search_school(body: ApiBase, request: Request):
    data = crudadapter.clss['school']().find(body)
    return templates.TemplateResponse('admin/school_card.html', {"request": request, "school_data": data})


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
    uvicorn.run(app, host='127.0.0.1', port=8000)
