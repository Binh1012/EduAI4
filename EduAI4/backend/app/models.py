"""Data model: Subject -> Topic -> Question, plus results and per-question answers."""
from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


def now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)
    password_hash = Column(String(100), nullable=False)
    role = Column(String(20), default="STUDENT", nullable=False)  # STUDENT | TEACHER | ADMIN
    created_at = Column(DateTime, default=now)


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    icon = Column(String(8), default="📘")
    color = Column(String(9), default="#2f7bff")
    topics = relationship("Topic", back_populates="subject", order_by="Topic.id")


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    name = Column(String(120), nullable=False)
    subject = relationship("Subject", back_populates="topics")
    questions = relationship("Question", back_populates="topic")


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False, index=True)
    text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # 2 options (true/false) or 4 options
    correct_index = Column(Integer, nullable=False)
    explanation = Column(Text, default="")
    difficulty = Column(Integer, default=1)  # 1 easy, 2 medium, 3 hard
    grade = Column(Integer, default=4)
    image_url = Column(String(500))
    audio_url = Column(String(500))
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=now)
    topic = relationship("Topic", back_populates="questions")


class QuizResult(Base):
    __tablename__ = "quiz_results"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    correct = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    xp = Column(Integer, default=0)
    created_at = Column(DateTime, default=now)


class UserAnswer(Base):
    __tablename__ = "user_answers"
    id = Column(Integer, primary_key=True)
    result_id = Column(Integer, ForeignKey("quiz_results.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    selected = Column(Integer, nullable=False)
    is_correct = Column(Boolean, nullable=False)
