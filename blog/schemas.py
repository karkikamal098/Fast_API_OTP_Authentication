from pydantic import BaseModel, EmailStr
from typing import Optional

# Input Schema
class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = True


#output Schema
class ShowBlog(BaseModel):
    title:str
    body:str
    published: Optional[bool] = True

    class Config:
        orm_mode = True


# User SignUp Schema
class UserSignUp(BaseModel):
    email: str
    password: str
    name: str

#User Response Schema (without password)
class ShowUser(BaseModel):
    email: str
    name: str

    class Config:
        orm_mode = True

# User Login Schema
class UserLogin(BaseModel):
    email: str
    password: str



# email otp works
class EmailRequest(BaseModel):
    email: EmailStr

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str

