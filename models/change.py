from pydantic import BaseModel

class ApiChangePassword(BaseModel):
    type: str
    old_password: str
    new_password: str


class ApiChangeEmail(BaseModel):
    type: str
    new_email: str