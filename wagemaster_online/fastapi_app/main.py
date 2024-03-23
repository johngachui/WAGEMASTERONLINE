# fastapi_app/main.py
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from . import schemas, crud, user_service
from .database import SessionLocal
from .dependencies import get_db

app = FastAPI()

@app.post("/employees/batch/", status_code=status.HTTP_201_CREATED)
def create_employee_batch(batch: schemas.EmployeeInBatch, db: Session = Depends(get_db)):
    for employee_in in batch.employees:
        # Step 1 & 2: Resolve CompanyIdentity and DivisionIdentity using CompanyKey and DivisionKey
        company = crud.get_company_by_key(db, employee_in.CompanyKey)
        division = crud.get_division_by_key(db, employee_in.DivisionKey)

        user = user_service.get_or_create_user_for_employee(db, employee_in)

        if not company or not division:
            raise HTTPException(status_code=404, detail="Company or Division not found")

        # Prepare employee data with resolved identities
        employee_data = {
            "CompanyIdentity": company.CompanyIdentity,
            "DivisionIdentity": division.DivisionIdentity,
            "CompanyKey": employee_in.CompanyKey,
            "EmployeeKey": employee_in.EmployeeKey,
            "StaffNo": employee_in.StaffNo,
            "StaffName": employee_in.StaffName,
            "Employed": employee_in.Employed,
            "Email": employee_in.Email,
            "needs_sync": False,  # Step 3: Set needs_sync to false
            "user_id": user.id
        }

        # Step 4: Create or update the employee record
        crud.create_or_update_employee(db, employee_data)

    return {"message": f"{len(batch.employees)} employees processed successfully"}

@app.post("/divisions/batch_update/", status_code=200)
async def batch_update_divisions(batch: schemas.DivisionUpdateBatch, db: Session = Depends(get_db)):
    for division_update in batch.divisions:
        company = crud.get_company_by_key(db, division_update.CompanyKey)
        if not company:
            raise HTTPException(status_code=404, detail=f"Company with key {division_update.CompanyKey} not found")
        division_data = {
            "CompanyIdentity": company.CompanyIdentity,
            "CompanyKey": division_update.CompanyKey,
            "DivisionKey": division_update.DivisionKey,
            "DivisionName": division_update.DivisionName
        }
        crud.create_or_update_division(db, division_data)
    return {"message": f"Processed {len(batch.divisions)} division updates"}