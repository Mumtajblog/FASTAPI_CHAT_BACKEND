from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from crud import create_message, create_session, create_user, get_messages_for_session, get_user_by_email
from auth import create_access_token, get_current_user
from hashing import verify_password
import models
import schemas
from database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.User)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@app.post("/sessions/", response_model=schemas.ChatSession)
def create_new_session(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_session(db=db, user_id=current_user.id)


@app.post("/sessions/{session_id}/messages/", response_model=schemas.Message)
def add_message_to_session(
    session_id: int,
    message: schemas.MessageCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_message(db=db, session_id=session_id, user_id=current_user.id, message=message)


@app.get("/sessions/{session_id}/messages/", response_model=list[schemas.Message])
def fetch_messages(
    session_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_messages_for_session(db, session_id=session_id, skip=skip, limit=limit)