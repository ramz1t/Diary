from pydantic import BaseModel

class ApiChangePassword(BaseModel):
    type: str
    old_pass: str
    new_pass: str


class ApiChangeEmail(BaseModel):
    type: str
    new_email: str