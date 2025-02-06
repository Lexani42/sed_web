from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.api import deps

router = APIRouter()

@router.get("/openers", response_model=List[schemas.Opener])
def get_openers(db: Session = Depends(deps.get_db)):
    return db.query(models.Opener).all()

@router.get("/openers/{opener_id}", response_model=schemas.Opener)
def get_opener(opener_id: int, db: Session = Depends(deps.get_db)):
    opener = db.query(models.Opener).filter(models.Opener.id == opener_id).first()
    if not opener:
        raise HTTPException(status_code=404, detail="Opener not found")
    return opener

@router.post("/openers", response_model=schemas.Opener)
def create_opener(opener: schemas.OpenerCreate, db: Session = Depends(deps.get_db)):
    db_opener = models.Opener(**opener.model_dump())
    db.add(db_opener)
    db.commit()
    db.refresh(db_opener)
    return db_opener

@router.put("/openers/{opener_id}", response_model=schemas.Opener)
def update_opener(
    opener_id: int, 
    opener: schemas.OpenerCreate, 
    db: Session = Depends(deps.get_db)
):
    db_opener = db.query(models.Opener).filter(models.Opener.id == opener_id).first()
    if not db_opener:
        raise HTTPException(status_code=404, detail="Opener not found")
    
    for key, value in opener.model_dump().items():
        setattr(db_opener, key, value)
    
    db.commit()
    db.refresh(db_opener)
    return db_opener

@router.delete("/openers/{opener_id}")
def delete_opener(opener_id: int, db: Session = Depends(deps.get_db)):
    db_opener = db.query(models.Opener).filter(models.Opener.id == opener_id).first()
    if not db_opener:
        raise HTTPException(status_code=404, detail="Opener not found")
    
    db.delete(db_opener)
    db.commit()
    return {"ok": True}

@router.post("/openers/{opener_id}/options", response_model=schemas.ContinueOption)
def create_continue_option(
    opener_id: int,
    option: schemas.ContinueOptionCreate,
    db: Session = Depends(deps.get_db)
):
    db_opener = db.query(models.Opener).filter(models.Opener.id == opener_id).first()
    if not db_opener:
        raise HTTPException(status_code=404, detail="Opener not found")
    
    db_option = models.ContinueOption(**option.model_dump(), opener_id=opener_id)
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return db_option

@router.delete("/openers/{opener_id}/options/{option_id}")
def delete_continue_option(
    opener_id: int,
    option_id: int,
    db: Session = Depends(deps.get_db)
):
    db_option = db.query(models.ContinueOption).filter(
        models.ContinueOption.id == option_id,
        models.ContinueOption.opener_id == opener_id
    ).first()
    
    if not db_option:
        raise HTTPException(status_code=404, detail="Continue option not found")
    
    db.delete(db_option)
    db.commit()
    return {"ok": True}
