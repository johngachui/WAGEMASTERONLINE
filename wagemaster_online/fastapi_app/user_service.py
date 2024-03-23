# fastapi_app/user_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import User, OneTimePassword  # Adjust the import path according to your project structure
from datetime import datetime
from passlib.hash import django_pbkdf2_sha256 as hasher

def get_or_create_user_for_employee(db: Session, employee_in):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == employee_in.Email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists as a username. Please use a different email.")
    
    # Generate a one-time password
    one_time_password = employee_in.StaffNo
    password_hash = hasher.hash(one_time_password)

    # Create a new user
    new_user = User(
        username=employee_in.Email,
        email=employee_in.Email,
        password=password_hash,  # You may need to hash the password depending on your setup
        user_type= 4
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
        
    # Create OneTimePassword record
    otp_record = OneTimePassword(
        user=new_user,
        otp=one_time_password,
        created_at=datetime.now(),
        used=False
    )
    db.add(otp_record)
    db.commit()

    return new_user
