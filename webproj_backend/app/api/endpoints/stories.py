from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app import schemas, models
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Story])
def get_stories(db: Session = Depends(deps.get_db)):
    return db.query(models.Story).all()

@router.get("/{story_id}", response_model=schemas.Story)
def get_story(story_id: int, db: Session = Depends(deps.get_db)):
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@router.post("/", response_model=schemas.Story)
def create_story(story: schemas.StoryCreate, db: Session = Depends(deps.get_db)):
    # Create story
    db_story = models.Story(title=story.title)
    db.add(db_story)
    db.commit()
    
    # Create format if it doesn't exist
    db_format = db.query(models.Format).filter(models.Format.type == story.format).first()
    if not db_format:
        db_format = models.Format(type=story.format)
        db.add(db_format)
        db.commit()
    
    # Add format to story
    db_story.formats.append(db_format)
    
    # Create language with content
    db_language = models.Language(code=story.language, story_id=db_story.id)
    db.add(db_language)
    db.commit()
    
    # Create content
    db_content = models.Content(
        content=story.content,
        language_id=db_language.id,
        format_id=db_format.id
    )
    db.add(db_content)
    db.commit()
    
    db.refresh(db_story)
    return db_story

@router.put("/{story_id}", response_model=schemas.Story)
def update_story(
    story_id: int,
    story: schemas.StoryUpdate,
    db: Session = Depends(deps.get_db)
):
    db_story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not db_story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    for key, value in story.model_dump().items():
        setattr(db_story, key, value)
    
    db.commit()
    db.refresh(db_story)
    return db_story

@router.delete("/{story_id}")
def delete_story(story_id: int, db: Session = Depends(deps.get_db)):
    db_story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not db_story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    db.delete(db_story)
    db.commit()
    return {"ok": True}

@router.post("/{story_id}/languages", response_model=schemas.Story)
async def add_language(
    story_id: int,
    language: str = Form(...),
    content: str = Form(...),
    format: str = Form(...),
    audio_file: UploadFile = File(None),
    db: Session = Depends(deps.get_db)
):
    db_story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not db_story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Create language if it doesn't exist for this story
    db_language = db.query(models.Language).filter(
        models.Language.story_id == story_id,
        models.Language.code == language
    ).first()
    
    if db_language:
        raise HTTPException(status_code=400, detail="Language already exists for this story")
    
    db_language = models.Language(code=language, story_id=story_id)
    db.add(db_language)
    db.commit()
    
    # Get or create format
    db_format = db.query(models.Format).filter(models.Format.type == format).first()
    if not db_format:
        db_format = models.Format(type=format)
        db.add(db_format)
        db.commit()
    
    # Add format to story if not already present
    if db_format not in db_story.formats:
        db_story.formats.append(db_format)
    
    # Create content
    content_value = content
    if format == 'audio' and audio_file:
        # Handle audio file upload here
        # Save file and store path in content_value
        pass
    
    db_content = models.Content(
        content=content_value,
        language_id=db_language.id,
        format_id=db_format.id
    )
    db.add(db_content)
    db.commit()
    
    db.refresh(db_story)
    return db_story

@router.delete("/{story_id}/languages/{language_code}")
def delete_language(
    story_id: int,
    language_code: str,
    db: Session = Depends(deps.get_db)
):
    db_language = db.query(models.Language).filter(
        models.Language.story_id == story_id,
        models.Language.code == language_code
    ).first()
    
    if not db_language:
        raise HTTPException(status_code=404, detail="Language not found")
    
    db.delete(db_language)
    db.commit()
    
    return {"ok": True}
