from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base

from .user import User
from .hospital import Hospital

Base = declarative_base()

# Association table
hospital_user_association = Table(
    "user_hospital",
    Base.metadata,
    Column("user_id", Integer, ForeignKey(User.id), primary_key=True),
    Column("hospital_id", Integer, ForeignKey(Hospital.id), primary_key=True),
)
