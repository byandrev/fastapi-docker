from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session, select
from .models import Note, NoteCreate
import json
import os

user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
port = os.getenv("DB_PORT")

engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}",
    echo=True
)

app = FastAPI()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {
        "message": "Welcome to the FastAPI application! "
        "You can use this API to manage your notes."
    }


@app.get("/notes")
async def get_notes():
    with Session(engine) as session:
        results = session.exec(select(Note)).all()

    return {"notes": results}


@app.post("/notes")
async def create_note(note: NoteCreate):
    if len(note.title) < 0 or len(note.content) < 0:
        return {"message": "Title and content can't be empty!"}


    with Session(engine) as session:
        db_nota = Note.model_validate(note)
        session.add(db_nota)
        session.commit()
        session.refresh(db_nota)

    return {"message": "Note created successfully!"}
