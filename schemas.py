from pydantic import BaseModel
from datetime import datetime


class MessageBase(BaseModel):
    text: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    created_at: datetime
    session_id: int
    user_id: int

    class Config:
        from_attributes = True


class ChatSessionBase(BaseModel):
    pass


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSession(ChatSessionBase):
    id: int
    user_id: int
    created_at: datetime
    messages: list[Message] = []

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    chat_sessions: list[ChatSession] = []
    messages: list[Message] = []

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
