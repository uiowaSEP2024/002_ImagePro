from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# Association table
user_hospital_association = Table(
    "user_hospital",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("hospital_id", Integer, ForeignKey("hospitals.id"), primary_key=True),
)
