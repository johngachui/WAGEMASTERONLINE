# fastapi_app/schemas.py
from pydantic import BaseModel, EmailStr

class EmployeeBase(BaseModel):
    StaffNo: str
    StaffName: str
    StaffIDNo: str
    Email: EmailStr
    Employed: bool

class EmployeeCreate(EmployeeBase):
    pass  # Extend this as needed
