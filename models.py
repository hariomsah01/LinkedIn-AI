from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    images: List["UserImage"] = Relationship(back_populates="owner")

class UserImage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    processed_filename: Optional[str]
    user_id: int = Field(foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="images")
