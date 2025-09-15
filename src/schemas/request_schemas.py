from pydantic import BaseModel, EmailStr

class SignUpRequest(BaseModel):
    email : EmailStr
    name : str
    password : str