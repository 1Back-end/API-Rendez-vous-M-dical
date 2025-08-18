from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean,Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.main.models.db.base_class import Base


class Religion(Base):

    __tablename__ = 'religions'

    uuid = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)

    added_by = Column(String, ForeignKey('users.uuid', ondelete="CASCADE"), nullable=False, index=True)
    user = relationship("User", backref="religions")

    is_active = Column(Boolean, nullable=False, index=True)
    is_deleted = Column(Boolean, nullable=False, index=True)

    created_at = Column(DateTime, nullable=False, index=True)
    updated_at = Column(DateTime, nullable=False, index=True)