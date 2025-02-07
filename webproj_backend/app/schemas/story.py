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

class Language(BaseModel):
    id: int
    code: str
    contents: List[Content]  # Keep as list in the model
    
    # Add a computed property for formatted contents
    @property
    def formatted_contents(self) -> Dict[str, str]:
        return {str(content.format_id): content.content for content in self.contents}

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
    languages: List[Language]
    formats: List[Format] = []

    class Config:
        from_attributes = True
