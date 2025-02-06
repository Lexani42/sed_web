from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class HobbyBase(BaseModel):
    name: str

class HobbyCreate(HobbyBase):
    pass

class Hobby(HobbyBase):
    id: int
    profile_id: int

    class Config:
        from_attributes = True

class NoteBase(BaseModel):
    key: str
    value: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    profile_id: int

    class Config:
        from_attributes = True

class ProfileBase(BaseModel):
    name: str
    age: int
    source: str
    telegram_tag: Optional[str] = None
    birth_date: Optional[date] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    source: Optional[str] = None
    telegram_tag: Optional[str] = None
    birth_date: Optional[date] = None

class Profile(ProfileBase):
    id: int
    hobbies: List[Hobby] = []
    notes: List[Note] = []

    class Config:
        from_attributes = True