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
    photo: Optional[str] = "avatar.jpg"
    opener_id: Optional[int] = None
    story_id: Optional[int] = None
    answered_opener: Optional[bool] = False
    story_discussed: Optional[bool] = False
    closed_for_meet: Optional[bool] = False
    closed_for_sex: Optional[bool] = False

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    source: Optional[str] = None
    telegram_tag: Optional[str] = None
    birth_date: Optional[date] = None
    photo: Optional[str] = None
    opener_id: Optional[int] = None
    story_id: Optional[int] = None
    answered_opener: Optional[bool] = None
    story_discussed: Optional[bool] = None
    closed_for_meet: Optional[bool] = None
    closed_for_sex: Optional[bool] = None

class Profile(ProfileBase):
    id: int
    hobbies: List[Hobby] = []
    notes: List[Note] = []
    photo_url: str

    class Config:
        from_attributes = True