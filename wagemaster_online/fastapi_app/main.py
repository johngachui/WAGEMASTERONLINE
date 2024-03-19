# fastapi_app/main.py
from fastapi import FastAPI
from .schemas import EmployeeBase, EmployeeCreate  # Adjust imports as necessary

app = FastAPI()

@app.post("/employee/")
async def create_employee(employee: EmployeeCreate):
    return {"employee_name": employee.StaffName}
