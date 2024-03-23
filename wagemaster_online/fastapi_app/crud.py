# fastapi_app/crud.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import Employee, Company, Division

def get_company_by_key(db: Session, key: str) -> Company:
    return db.query(Company).filter(Company.CompanyKey == key).first()

def get_division_by_key(db: Session, key: str) -> Division:
    return db.query(Division).filter(Division.DivisionKey == key).first()

def create_or_update_employee(db: Session, employee_data: dict):
    # Look up Company by CompanyKey
    company = db.query(Company).filter(Company.CompanyKey == employee_data["CompanyKey"]).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Check if an Employee with the given EmployeeKey exists
    employee = db.query(Employee).filter(Employee.EmployeeKey == employee_data["EmployeeKey"]).first()

    if employee:
        # If Employee exists but belongs to a different company, return an error
        if employee.CompanyIdentity != company.CompanyIdentity:
            raise HTTPException(status_code=400, detail="Employee in another company")
        # Otherwise, update the existing employee record
        for key, value in employee_data.items():
            if key != "CompanyKey":  # Skip the CompanyKey since we've already resolved it to CompanyIdentity
                setattr(employee, key, value if key != 'CompanyIdentity' else company.CompanyIdentity)
    else:
        # If Employee doesn't exist, create a new one
        new_employee_data = {k: v for k, v in employee_data.items() if k != "CompanyKey"}
        new_employee_data['CompanyIdentity'] = company.CompanyIdentity  # Set CompanyIdentity to the resolved value
        employee = Employee(**new_employee_data)
        db.add(employee)

    db.commit()
    db.refresh(employee)
    return employee

def create_or_update_division(db: Session, division_data: dict):
    division = get_division_by_key(db, division_data['DivisionKey'])
    if division:
        # Update existing division
        for key, value in division_data.items():
            setattr(division, key, value)
    else:
        # Create new division
        division = Division(**division_data)
        db.add(division)
    db.commit()
    db.refresh(division)
    return division