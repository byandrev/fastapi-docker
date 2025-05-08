from typing import Annotated
from sqlmodel import Field, SQLModel

class NoteBase(SQLModel):
    title: str = Field(default=None, nullable=False)
    content: str = Field(default=None, nullable=False)

class Note(NoteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class NoteCreate(NoteBase):
    pass
