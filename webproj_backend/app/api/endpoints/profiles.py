from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Profile])
def get_profiles(db: Session = Depends(deps.get_db)):
    return db.query(models.Profile).all()

@router.get("/{profile_id}", response_model=schemas.Profile)
def get_profile(profile_id: int, db: Session = Depends(deps.get_db)):
    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/", response_model=schemas.Profile)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(deps.get_db)):
    db_profile = models.Profile(**profile.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.put("/{profile_id}", response_model=schemas.Profile)
def update_profile(
    profile_id: int,
    profile: schemas.ProfileUpdate,
    db: Session = Depends(deps.get_db)
):
    db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    profile_data = profile.model_dump(exclude_unset=True)
    for key, value in profile_data.items():
        setattr(db_profile, key, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.delete("/{profile_id}")
def delete_profile(profile_id: int, db: Session = Depends(deps.get_db)):
    db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    db.delete(db_profile)
    db.commit()
    return {"ok": True}

# Hobby endpoints
@router.post("/{profile_id}/hobbies", response_model=schemas.Hobby)
def create_hobby(
    profile_id: int,
    hobby: schemas.HobbyCreate,
    db: Session = Depends(deps.get_db)
):
    db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    db_hobby = models.Hobby(**hobby.model_dump(), profile_id=profile_id)
    db.add(db_hobby)
    db.commit()
    db.refresh(db_hobby)
    return db_hobby

@router.delete("/{profile_id}/hobbies/{hobby_id}")
def delete_hobby(
    profile_id: int,
    hobby_id: int,
    db: Session = Depends(deps.get_db)
):
    db_hobby = db.query(models.Hobby).filter(
        models.Hobby.id == hobby_id,
        models.Hobby.profile_id == profile_id
    ).first()
    if not db_hobby:
        raise HTTPException(status_code=404, detail="Hobby not found")
    
    db.delete(db_hobby)
    db.commit()
    return {"ok": True}

# Note endpoints
@router.post("/{profile_id}/notes", response_model=schemas.Note)
def create_note(
    profile_id: int,
    note: schemas.NoteCreate,
    db: Session = Depends(deps.get_db)
):
    # Trim and validate input
    key = note.key.strip()
    value = note.value.strip()
    
    if not key or not value:
        raise HTTPException(
            status_code=400,
            detail="Note key and value cannot be empty"
        )
    
    db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    db_note = models.Note(
        key=key,
        value=value,
        profile_id=profile_id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.put("/{profile_id}/notes/{note_id}", response_model=schemas.Note)
def update_note(
    profile_id: int,
    note_id: int,
    note: schemas.NoteCreate,
    db: Session = Depends(deps.get_db)
):
    # Trim and validate input
    key = note.key.strip()
    value = note.value.strip()
    
    if not key or not value:
        raise HTTPException(
            status_code=400,
            detail="Note key and value cannot be empty"
        )
    
    db_note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.profile_id == profile_id
    ).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db_note.key = key
    db_note.value = value
    
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/{profile_id}/notes/{note_id}")
def delete_note(
    profile_id: int,
    note_id: int,
    db: Session = Depends(deps.get_db)
):
    db_note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.profile_id == profile_id
    ).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(db_note)
    db.commit()
    return {"ok": True}
