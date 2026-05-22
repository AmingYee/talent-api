from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class TalentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    title: str = Field(..., description="The talent Job title")
    profile_text: str = Field(..., description="A short introduction to the talent")
    email: EmailStr
    phone: str = Field(..., min_length=1, max_length=50)
    city: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    github: Optional[str] = None
    linkedin: Optional[str] = None

class TalentCreate(TalentBase):
    pass

class TalentResponse(TalentBase):
    id: str
    
    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: str
    talent_id: str
    
    class Config:
        from_attributes = True