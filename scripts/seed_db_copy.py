import sys
import os
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import engine, SessionLocal, Base
from app.models import Talent, Document

YOUR_INFO = {
    "name": "Placeholder",
    "email": "Placeholder",
    "phone": "Placeholder",
    "city": "Placeholder",
    "country": "Placeholder",
    "github": "Placeholder",
    "linkedin": "Placeholder",
    "title": "Placeholder",
    "profile_text": (
        "Placeholder"
    ),
    
    "cover_letter": """Placeholder""",

    "skills": f"""Placeholder""",

    "projects": f"""Placeholder
""",
}

def seed_database():
    """Create and seed the database with your information"""
    
    print("=" * 60)
    print(" Seeding Talent API Database with your information ")
    print("=" * 60)
    
    print("\nCreating database...")
    
    Base.metadata.drop_all(bind=engine)
    
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        print("Seeding your information")
        talent = Talent(
            name=YOUR_INFO["name"],
            email=YOUR_INFO["email"],
            phone=YOUR_INFO["phone"],
            city=YOUR_INFO["city"],
            country=YOUR_INFO["country"],
            github=YOUR_INFO.get("github"),
            linkedin=YOUR_INFO.get("linkedin"),
            title=YOUR_INFO["title"],
            profile_text=YOUR_INFO["profile_text"]
        )
        db.add(talent)
        db.flush()
        
        print(f"Created talent profile: {YOUR_INFO['name']}")
        print(f"{YOUR_INFO['email']}")
        print(f"{YOUR_INFO['github']}")
        print(f"ID: {talent.id}")
        
        cover_letter = Document(
            talent_id=talent.id,
            name="Placeholder - Ansøgning",
            content=YOUR_INFO["cover_letter"]
        )
        db.add(cover_letter)
        print(f"Added document: {cover_letter.name}")
        
        skills_doc = Document(
            talent_id=talent.id,
            name="Placeholder",
            content=YOUR_INFO["skills"]
        )
        db.add(skills_doc)
        print(f"Added document: {skills_doc.name}")
        
        projects_doc = Document(
            talent_id=talent.id,
            name="Placeholder",
            content=YOUR_INFO["projects"]
        )
        db.add(projects_doc)
        print(f"Added document: {projects_doc.name}")
        
        db.commit()
        
        print("\n" + "=" * 60)
        print("  Database seeded successfully!")
        
    except Exception as e:
        print(f"\nFejl ved seeding af database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Talent API Database Seeder")
    print("\n" + "=" * 60)
    
    seed_database()