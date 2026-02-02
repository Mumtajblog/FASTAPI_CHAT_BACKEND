from sqlalchemy.orm import Session

import models
import schemas
from hashing import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_session(db: Session, user_id: int):
    db_session = models.ChatSession(user_id=user_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def create_message(db: Session, session_id: int, user_id: int, message: schemas.MessageCreate):
    db_message = models.Message(**message.dict(), session_id=session_id, user_id=user_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_messages_for_session(db: Session, session_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Message)
        .filter(models.Message.session_id == session_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
