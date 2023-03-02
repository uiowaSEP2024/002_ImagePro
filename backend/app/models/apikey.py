from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Apikey(Base):
    __tablename__ = "apikeys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    key = Column(String, unique=True)

    user = relationship("User", back_populates='apikeys')
