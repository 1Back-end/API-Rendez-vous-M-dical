from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.main.models.db.base_class import Base

class Address(Base):
    """ Address Model for storing user addresses related details """
    __tablename__ = "addresses"

    uuid = Column(String, primary_key=True, unique=True)
    street = Column(String, nullable=False, default="")
    city = Column(String, nullable=False, default="")
    state = Column(String, default="")
    zipcode = Column(String, nullable=False, default="")
    country = Column(String, nullable=False, default="")
    apartment_number = Column(String, default="")
    additional_information = Column(String, default="")
    
    date_added = Column(DateTime, server_default=func.now())
    date_modified = Column(DateTime, server_default=func.now())
