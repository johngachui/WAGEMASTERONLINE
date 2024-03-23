# fastapi_app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean,Date, Text, DECIMAL,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime, timedelta

Base = declarative_base()

class User(Base):
    __tablename__ = 'wagemaster_online_user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Store hashed passwords
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime(timezone=True), server_default=func.now())
    user_type = Column(Integer)
    
    one_time_passwords = relationship("OneTimePassword", back_populates="user")


class OneTimePassword(Base):
    __tablename__ = 'wagemaster_online_onetimepassword'
    id = Column(Integer, primary_key=True, index=True)
    otp = Column(String(10), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    used = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('wagemaster_online_user.id'), nullable=False)

    user = relationship("User", back_populates="one_time_passwords")

    @property
    def is_expired(self):
        return datetime.utcnow() > self.created_at + timedelta(minutes=1440)
    
class ClientGroup(Base):
    __tablename__ = 'client_group'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    clients = relationship("Client", back_populates="client_group")

class Client(Base):
    __tablename__ = 'client'
    ClientIdentity = Column(Integer, primary_key=True, autoincrement=True)
    ClientName = Column(String(255))
    ClientEmail = Column(String(255))
    ClientTel = Column(String(20))
    ClientContactPerson = Column(String(255))
    # Relationships
    client_group_id = Column(Integer, ForeignKey('client_group.id'))
    client_group = relationship(ClientGroup, back_populates="clients")
    # For many-to-many, define an association table and relationship

class Company(Base):
    __tablename__ = 'company'
    CompanyIdentity = Column(Integer, primary_key=True, autoincrement=True)
    CompanyName = Column(Text)
    CompanyEmail = Column(String(255))
    CompanyTel = Column(Text)
    CompanyContactPerson = Column(Text)
    CompanyKey = Column(Text, default="n/a")
    needs_sync = Column(Boolean, default=True)
    ClientIdentity = Column(Integer, ForeignKey('client.ClientIdentity'))
    client = relationship(Client)

class Division(Base):
    __tablename__ = 'division'
    DivisionIdentity = Column(Integer, primary_key=True, autoincrement=True)
    CompanyIdentity = Column(Integer, ForeignKey('company.CompanyIdentity'))
    DivisionName = Column(String(255))
    CompanyKey = Column(Text, default="n/a")
    DivisionKey = Column(Text, default="n/a")
    company = relationship(Company)

class Employee(Base):
    __tablename__ = 'employee'
    StaffIdentity = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('wagemaster_online_user.id'))  # Adjust as necessary
    CompanyIdentity = Column(Integer, ForeignKey('company.CompanyIdentity'))
    DivisionIdentity = Column(Integer, ForeignKey('division.DivisionIdentity'))
    StaffNo = Column(String(255))
    StaffName = Column(String(255))
    Email = Column(String(255))
    Employed = Column(Boolean)
    EmployeeKey = Column(Text, default="n/a")
    needs_sync = Column(Boolean, default=True)
    # Relationships
    company = relationship(Company)
    division = relationship(Division)
    user = relationship(User)  # Assuming a relationship here
    leave_balance = relationship("LeaveBalance", back_populates="employee", uselist=False)
    processed_leaves = relationship("ProcessedLeave", back_populates="employee")
    leave_applications = relationship("LeaveApplication", back_populates="employee")
    
class LeaveBalance(Base):
    __tablename__ = 'leavebalance'
    # Use the Employee's StaffIdentity as the primary key for LeaveBalance
    StaffIdentity = Column(Integer, ForeignKey('employee.StaffIdentity'), primary_key=True)
    AnnualBfwd = Column(DECIMAL(10, 2))
    AnnualCfwd = Column(DECIMAL(10, 2))
    Earned = Column(DECIMAL(10, 2))
    Taken = Column(DECIMAL(10, 2))
    Sold = Column(DECIMAL(10, 2))
    Adjustment = Column(DECIMAL(10, 2))
    Absence = Column(DECIMAL(10, 2))
    OffsBfwd = Column(DECIMAL(10, 2))
    OffsCfwd = Column(DECIMAL(10, 2))
    MaternityBfwd = Column(DECIMAL(10, 2))
    MaternityCfwd = Column(DECIMAL(10, 2))
    SickFull = Column(DECIMAL(10, 2))
    SickHalf = Column(DECIMAL(10, 2))
    EmployeeKey = Column(Text, default="n/a")
    needs_sync = Column(Boolean, default=True)
    # Define the reverse of the one-to-one relationship with Employee
    employee = relationship("Employee", back_populates="leave_balance")

class ProcessedLeave(Base):
    __tablename__ = 'processedleave'
    id = Column(Integer, primary_key=True, index=True)
    StaffIdentity = Column(Integer, ForeignKey('employee.StaffIdentity'))
    LeaveType = Column(Text)
    StartDate = Column(Date)
    StopDate = Column(Date)
    Approved = Column(Boolean)
    NotApproved = Column(Boolean)
    Taken = Column(Boolean)
    EmployeeKey = Column(Text, default="n/a")
    needs_sync = Column(Boolean, default=True)
    employee = relationship("Employee", back_populates="processed_leaves")

class LeaveApplication(Base):
    __tablename__ = 'leaveapplication'
    id = Column(Integer, primary_key=True, index=True)
    StaffIdentity = Column(Integer, ForeignKey('employee.StaffIdentity'))
    LeaveType = Column(Text)
    StartDate = Column(Date)
    StopDate = Column(Date)
    EmployeeKey = Column(Text, default="n/a")
    needs_sync = Column(Boolean, default=True)
    employee = relationship("Employee", back_populates="leave_applications")

