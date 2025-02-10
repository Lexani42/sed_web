from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app.models.dialog import Opener, ContinueOption
from app.models.profile import Profile, Hobby, Note
from app.models.story import Story, Language, Format, Content
from pathlib import Path

def init_db():
    # Create avatars directory and copy default avatar
    avatar_dir = Path("app/static/avatars")
    avatar_dir.mkdir(parents=True, exist_ok=True)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if database is already initialized
        if db.query(Format).first():
            return
            
        # Initialize basic formats
        formats = [
            Format(type="text"),
            Format(type="audio")
        ]
        db.add_all(formats)
        
        # Initialize some example openers
        openers = [
            Opener(
                text="Hello! How are you today?",
                context="greeting",
                continue_options=[
                    ContinueOption(text="I'm doing great!", weight=1.0),
                    ContinueOption(text="Not bad, thanks.", weight=1.0)
                ]
            ),
            Opener(
                text="Would you like to hear a story?",
                context="story_start",
                continue_options=[
                    ContinueOption(text="Yes, please!", weight=1.0),
                    ContinueOption(text="Maybe later.", weight=0.5)
                ]
            )
        ]
        db.add_all(openers)
        
        # Initialize example profiles
        profiles = [
            Profile(
                name="John Doe",
                age=30,
                source="example",
                photo="avatar.jpg",
                opener_id=1,  # Reference to the first opener
                story_id=1,   # Reference to the welcome story
                answered_opener=True,
                story_discussed=True,
                closed_for_meet=False,
                closed_for_sex=False,
                hobbies=[
                    Hobby(name="Reading"),
                    Hobby(name="Writing")
                ],
                notes=[
                    Note(key="favorite_color", value="blue"),
                    Note(key="preferred_language", value="English")
                ]
            )
        ]
        db.add_all(profiles)
        
        # Initialize example stories
        stories = [
            Story(
                title="Welcome Story",
                languages=[
                    Language(
                        code="en",
                        contents=[
                            Content(
                                content="Welcome to our story platform!",
                                format_id=1  # text format
                            )
                        ]
                    )
                ]
            )
        ]
        db.add_all(stories)
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close() 