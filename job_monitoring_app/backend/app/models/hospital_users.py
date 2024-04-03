from sqlalchemy import Column, Integer, ForeignKey
from .base import Base
from .user import User
from .hospital import Hospital


class HospitalUsers(Base):
    """
    Represents the association between users and hospitals.
    """

    __tablename__ = "user_hospital"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    hospital_id = Column(Integer, ForeignKey(Hospital.id, ondelete="CASCADE"))
