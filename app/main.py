from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from contextlib import asynccontextmanager
import uuid

from app.database import get_db, engine, Base
from app.models import Talent as TalentModel, Document as DocumentModel
from app.schemas import TalentCreate, TalentResponse, DocumentCreate, DocumentResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Talent API",
    description="REST API for managing talent profiles and documents",
    version="1.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Talent API",
        "documentation": "/docs",
        "endpoints": {
            "GET /talent": "Get all talents",
            "GET /talent/{id}": "Get specific talent",
            "GET /talent/{id}/documents": "Get talent's documents",
            "GET /talent/{id}/documents/{doc_id}": "Get specific document",
        }
    }

@app.get("/talent", response_model=List[TalentResponse], tags=["Talent"])
async def get_talents(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    talents = db.query(TalentModel).offset(skip).limit(limit).all()
    return talents

@app.get("/talent/{talent_id}", response_model=TalentResponse, tags=["Talent"])
async def get_talent(talent_id: str, db: Session = Depends(get_db)):  # Changed to str
    """Get a specific talent by ID"""
    talent = db.query(TalentModel).filter(TalentModel.id == talent_id).first()
    if not talent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Talent with id {talent_id} not found"
        )
    return talent

@app.post("/talent", response_model=TalentResponse, status_code=status.HTTP_201_CREATED, tags=["Talent"])
async def create_talent(talent: TalentCreate, db: Session = Depends(get_db)):
    existing = db.query(TalentModel).filter(TalentModel.email == talent.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Talent with email {talent.email} already exists"
        )
    
    db_talent = TalentModel(
        id=str(uuid.uuid4()),
        **talent.model_dump()
    )
    db.add(db_talent)
    db.commit()
    db.refresh(db_talent)
    return db_talent

@app.get("/talent/{talent_id}/documents", response_model=List[DocumentResponse], tags=["Documents"])
async def get_talent_documents(
    talent_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):

    talent = db.query(TalentModel).filter(TalentModel.id == talent_id).first()
    if not talent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Talent with id {talent_id} not found"
        )
    
    documents = db.query(DocumentModel).filter(
        DocumentModel.talent_id == talent_id
    ).offset(skip).limit(limit).all()
    return documents

@app.get("/talent/{talent_id}/documents/{doc_id}", response_model=DocumentResponse, tags=["Documents"])
async def get_talent_document(
    talent_id: str,
    doc_id: str,
    db: Session = Depends(get_db)
):
    document = db.query(DocumentModel).filter(
        DocumentModel.id == doc_id,
        DocumentModel.talent_id == talent_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {doc_id} not found for talent {talent_id}"
        )
    return document

@app.post("/talent/{talent_id}/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED, tags=["Documents"])
async def create_talent_document(
    talent_id: str,
    document: DocumentCreate,
    db: Session = Depends(get_db)
):
    talent = db.query(TalentModel).filter(TalentModel.id == talent_id).first()
    if not talent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Talent with id {talent_id} not found"
        )
    
    db_document = DocumentModel(
        id=str(uuid.uuid4()),
        talent_id=talent_id,
        **document.model_dump()
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

@app.delete("/talent/{talent_id}/documents/{doc_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Documents"])
async def delete_talent_document(
    talent_id: str,
    doc_id: str,
    db: Session = Depends(get_db)
):
    document = db.query(DocumentModel).filter(
        DocumentModel.id == doc_id,
        DocumentModel.talent_id == talent_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {doc_id} not found for talent {talent_id}"
        )
    
    db.delete(document)
    db.commit()