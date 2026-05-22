from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

class Talent(Base):
    __tablename__ = "talents"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    profile_text = Column(Text, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    github = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    
    documents = relationship("Document", back_populates="talent", cascade="all, delete-orphan")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    talent_id = Column(String(36), ForeignKey("talents.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    
    talent = relationship("Talent", back_populates="documents")