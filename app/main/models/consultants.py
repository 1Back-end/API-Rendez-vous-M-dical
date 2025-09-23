from datetime import datetime
from operator import index
from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean,Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.main.models.db.base_class import Base



class Consultants(Base):
    __tablename__ = 'consultants'

    uuid = Column(String, primary_key=True,index=True)
    first_name = Column(String,nullable=False,index=True)
    last_name = Column(String,nullable=False,index=True)
    phone_number = Column(String,nullable=False,index=True,unique=True)
    phone_number_2 = Column(String,nullable=True,index=True,unique=True)
    email = Column(String,nullable=False,index=True)

    titre_uuid = Column(String,ForeignKey('titres.uuid'),nullable=False,index=True)
    titre = relationship('Titre',foreign_keys=[titre_uuid])

    service_hopital_uuid = Column(String,ForeignKey('service_hopitals.uuid'),nullable=False,index=True)
    service_hopital = relationship('ServiceHopitals',foreign_keys=[service_hopital_uuid])

    specialite_uuid = Column(String,ForeignKey('specialites.uuid'),nullable=False,index=True)
    specialite = relationship('Specialites',foreign_keys=[specialite_uuid])

    added_by = Column(String, ForeignKey('users.uuid', ondelete="CASCADE"), nullable=False, index=True)
    user = relationship("User", foreign_keys=[added_by])

    is_active = Column(Boolean, nullable=False, index=True)
    is_deleted = Column(Boolean, nullable=False, index=True)

    created_at = Column(DateTime, nullable=False, index=True)
    updated_at = Column(DateTime, nullable=False, index=True)