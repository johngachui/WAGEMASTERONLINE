# fastapi_app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import List

class EmployeeIn(BaseModel):
    CompanyKey: str
    DivisionKey: str
    EmployeeKey: str
    StaffNo: str
    StaffName: str
    Employed: bool
    Email: EmailStr

class EmployeeInBatch(BaseModel):
    employees: list[EmployeeIn]

class DivisionUpdateItem(BaseModel):
    CompanyKey: str
    DivisionKey: str
    DivisionName: str

class DivisionUpdateBatch(BaseModel):
    divisions: List[DivisionUpdateItem]