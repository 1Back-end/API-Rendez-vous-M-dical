from datetime import datetime
from operator import index

from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean,Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.main.models.db.base_class import Base



class Patient(Base):

    __tablename__ = 'patient'


    uuid = Column(String, primary_key=True, index=True)

    first_name = Column(String,nullable=False,index=True)
    last_name = Column(String,nullable=False,index=True)
    phone_number = Column(String,nullable=False,index=True)
    phone_number_2 = Column(String,nullable=True,index=True)
    email = Column(String,nullable=True,index=True)

    address_uuid = Column(String, ForeignKey('addresses.uuid', ondelete="CASCADE"), nullable=False, index=True)
    address = relationship("Address", foreign_keys=[address_uuid])

    sexe_uuid = Column(String, ForeignKey('sexes.uuid', ondelete="CASCADE"), nullable=False, index=True)
    sexe = relationship("Sexe", foreign_keys=[sexe_uuid])

    religion_uuid = Column(String, ForeignKey('religions.uuid', ondelete="CASCADE"),nullable=False, index=True)
    religion = relationship("Religion", foreign_keys=[religion_uuid])

    added_by = Column(String, ForeignKey('users.uuid', ondelete="CASCADE"), nullable=False, index=True)
    user = relationship("User",foreign_keys=[added_by])

    is_patient_confidentiel= Column(Boolean, nullable=False, index=True)
    is_active = Column(Boolean,default=True, nullable=False, index=True)

    created_at = Column(DateTime, default=func.now())  # Account creation timestamp
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Last update timestamp
    is_deleted = Column(Boolean, default=False)  # Soft delete flag
