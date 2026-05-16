from sqlalchemy.orm import sessionmaker
from database.db import engine
from database.models import User, Resume
from utils.auth import hash_password, verify_password

SessionLocal = sessionmaker(bind=engine)


def get_user_by_email(email):
    session=SessionLocal()

    try:
        return session.query(
            User
        ).filter_by(email=email ).first() 
    
    finally:
        session.close()


def register_user(name, email, password_hash):
    session = SessionLocal()
    try:
        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            return None

        new_user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            is_verified=1
        )

        session.add(new_user)
        session.commit()
        return new_user
    finally:
        session.close()


def authenticate_user(email, password):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(email=email).first()
        if not user:
            return None

        if user.password_hash:
            if verify_password(password, user.password_hash):
                return user
            return None

        if user.otp and password == user.otp:
            user.password_hash = hash_password(password)
            user.otp = None
            user.is_verified = 1
            session.commit()
            return user

        return None
    finally:
        session.close()


def save_resume(user_email, target_role, generated_resume, ats_score, readiness_score):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(email=user_email).first()
        if not user:
            return None
        new_resume = Resume(
            user_id=user.id,
            target_role=target_role,
            generated_resume=generated_resume,
            ats_score=ats_score,
            readiness_score=readiness_score,
        )
        session.add(new_resume)
        session.commit()
        return new_resume
    finally:
        session.close()


def get_user_resumes(user_email):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(email=user_email).first()
        if not user:
            return []
        return session.query(Resume).filter_by(user_id=user.id).all()
    finally:
        session.close()


def delete_resume(resume_id):
    session = SessionLocal()
    try:
        resume = session.query(Resume).filter_by(id=resume_id).first()
        if resume:
            session.delete(resume)
            session.commit()
            return True
        return False
    finally:
        session.close()
