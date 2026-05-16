from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Float,
    ForeignKey
)

from sqlalchemy.orm import declarative_base 
from datetime import datetime 
from sqlalchemy.orm import relationship

Base=declarative_base()

class User(Base):
    __tablename__="users"

    id=Column(
        Integer,
        primary_key=True
    )

    name=Column(String(255),nullable=True)

    is_verified=Column(
        Integer,
        default=0
    )

    email=Column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash=Column(
        String(255),
        nullable=True
    )

    otp=Column(
        String(10)
    )

    created_at=Column(
        DateTime,
        default=datetime.utcnow
    )


    resumes=relationship(
        "Resume",
        back_populates="user"
    )


class Resume(Base):
    __tablename__='resumes'

    id=Column(
        Integer,
        primary_key=True
    )

    user_id=Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False 
    )

    target_role=Column(
        String(255),
        nullable=False 
    )

    generated_resume=Column(
        Text,
        nullable=False
    )

    ats_score=Column(
        Float,
        nullable=True
    )

    readiness_score=Column(
        Float,
        nullable=True
    )

    created_at=Column(
        DateTime,
        default=datetime.utcnow
    )


    user=relationship(
        "User",
        back_populates="resumes"
    )