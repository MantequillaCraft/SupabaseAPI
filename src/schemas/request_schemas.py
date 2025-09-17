from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class SignUpRequest(BaseModel):
    email : EmailStr
    name : str
    password : str


class AssignmentsFilters(BaseModel):
    createdAtMax : Optional[datetime] = None
    createdAtMin : Optional[datetime] = None
    status : Optional[str] = None