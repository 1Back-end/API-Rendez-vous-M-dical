from datetime import datetime
from operator import index

from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean,Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.main.models.db.base_class import Base



class Patient(Base):

    __tablename__ = 'patients'


    uuid = Column(String, primary_key=True, index=True)

    first_name = Column(String,nullable=False,index=True)
    last_name = Column(String,nullable=False,index=True)
    phone_number = Column(String,nullable=False,index=True)
    phone_number_2 = Column(String,nullable=True,index=True)
    email = Column(String,nullable=False,index=True)

    address_uuid = Column(String, ForeignKey('addresses.uuid', ondelete="CASCADE"), nullable=False, index=True)
    address = relationship("Address", backref="patients")

    sexe_uuid = Column(String, ForeignKey('sexes.uuid', ondelete="CASCADE"), nullable=False, index=True)
    sexe = relationship("Sexe", backref="patients")

    religion_uuid = Column(String, ForeignKey('religions.uuid', ondelete="CASCADE"),nullable=False, index=True)
    religion = relationship("Religion", backref="patients")

    added_by = Column(String, ForeignKey('users.uuid', ondelete="CASCADE"), nullable=False, index=True)
    user = relationship("User", backref="hopitals")

    is_patient_confidentiel= Column(Boolean, nullable=False, index=True)

    is_active = Column(Boolean, nullable=False, index=True)
    is_deleted = Column(Boolean, nullable=False, index=True)

    created_at = Column(DateTime, nullable=False, index=True)
    updated_at = Column(DateTime, nullable=False, index=True)
