# Talent API

A REST API for managing talent profiles and documents, built with FastAPI and containerized with Docker.

## Instructions

Change the placeholder text in seed_db_copy.py and run it once 
```powershell
python scripts/seed_db_copy.py
```
you should now have a talent.db file with your information startup the container with

```powershell
docker compose up -d 
```

test everything i working with 
```powershell
curl http://localhost:8000/talent/
```

## Tech Stack

- **Python 3.12** - Programming language
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database
- **Docker** - Containerization
- **Uvicorn** - ASGI server
