from pydantic import BaseModel
from typing import Union


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class AuthUser(BaseModel):
    username: str


class UserInDB(AuthUser):
    hashed_password: str
