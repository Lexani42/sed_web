from pydantic import BaseModel
from typing import List, Optional

class ContinueOptionBase(BaseModel):
    text: str
    weight: float = 1.0

class ContinueOptionCreate(ContinueOptionBase):
    pass

class ContinueOption(ContinueOptionBase):
    id: int
    opener_id: int

    class Config:
        from_attributes = True

class OpenerBase(BaseModel):
    text: str
    context: str

class OpenerCreate(OpenerBase):
    pass

class Opener(OpenerBase):
    id: int
    continue_options: List[ContinueOption] = []

    class Config:
        from_attributes = True
