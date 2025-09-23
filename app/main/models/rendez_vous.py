from datetime import datetime

from psycopg2 import Date
from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean, Integer, func, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.main.models.db.base_class import Base
from enum import Enum


class RendezVousStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    closed = "closed"


class Rendez_Vous(Base):

    __tablename__ = "rendez_vous"

    uuid = Column(String, primary_key=True,index=True)

    consultant_uuid = Column(String, ForeignKey("consultants.uuid"), nullable=False,index=True)
    consultant = relationship("Consultants", foreign_keys=[consultant_uuid])

    patient_uuid = Column(String, ForeignKey("patients.uuid"), nullable=False,index=True)
    patient = relationship("Patient", foreign_keys=[patient_uuid])

    date_rendez_vous = Column(DateTime, nullable=False)

    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    status = Column(String, nullable=False,default=RendezVousStatus.pending)
    is_active = Column(Boolean, nullable=False, index=True,default=True)
    is_deleted = Column(Boolean, nullable=False, index=True,default=False)

    created_at = Column(DateTime, default=func.now())  # Account creation timestamp
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Last update timestamp

