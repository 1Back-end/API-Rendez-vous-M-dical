from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean,Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.main.models.db.base_class import Base



class Hopitals(Base):

    __tablename__ = 'hopitals'


    uuid = Column(String, primary_key=True,index=True)
    name = Column(String,nullable=False,unique=True,index=True)
    abbrevation = Column(String,nullable=False,unique=True,index=True)

    address_uuid = Column(String,ForeignKey('addresses.uuid',ondelete="CASCADE"),nullable=False,index=True)
    address = relationship("Address", backref="hopitals")


    added_by = Column(String,ForeignKey('users.uuid',ondelete="CASCADE"),nullable=False,index=True)
    user = relationship("User", backref="hopitals")

    is_active = Column(Boolean,nullable=False,index=True)
    is_deleted = Column(Boolean,nullable=False,index=True)

    created_at = Column(DateTime,nullable=False,index=True)
    updated_at = Column(DateTime,nullable=False,index=True)
