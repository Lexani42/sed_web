from pydantic import BaseModel
from typing import List, Dict, Optional

class ContentBase(BaseModel):
    content: str

class Content(ContentBase):
    id: int
    language_id: int
    format_id: int

    class Config:
        from_attributes = True

class FormatBase(BaseModel):
    type: str  # 'text' or 'audio'

class Format(FormatBase):
    id: int

    class Config:
        from_attributes = True

class LanguageBase(BaseModel):
    code: str
    contents: Dict[str, str]  # format_type -> content mapping

class LanguageCreate(LanguageBase):
    pass

class Language(LanguageBase):
    id: int
    story_id: int

    class Config:
        from_attributes = True

class StoryBase(BaseModel):
    title: str

class StoryCreate(StoryBase):
    content: str
    language: str
    format: str

class StoryUpdate(StoryBase):
    pass

class Story(StoryBase):
    id: int
    languages: List[Language] = []
    formats: List[Format] = []

    class Config:
        from_attributes = True
