from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class RegisterIn(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=6, max_length=64)


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=64)


class TokenOut(BaseModel):
    access_token: str
    name: str
    role: str


class TopicOut(BaseModel):
    id: int
    name: str
    accuracy: Optional[int] = None


class SubjectOut(BaseModel):
    id: int
    name: str
    icon: str
    color: str
    topics: List[TopicOut]


class QuestionOut(BaseModel):
    id: int
    text: str
    options: List[str]
    correct_index: int
    explanation: str


class AnswerIn(BaseModel):
    question_id: int
    selected: int = Field(ge=0, le=3)


class SubmitIn(BaseModel):
    topic_id: int
    answers: List[AnswerIn] = Field(min_length=1, max_length=50)


class ResultOut(BaseModel):
    correct: int
    total: int
    percent: int
    xp_gained: int


class TopicStat(BaseModel):
    topic_id: int
    topic: str
    subject: str
    accuracy: int
    total: int


class SubjectStat(BaseModel):
    subject: str
    accuracy: Optional[int] = None


class ProgressOut(BaseModel):
    xp: int
    level: int
    streak: int
    quizzes_done: int
    perfect_quizzes: int
    subjects: List[SubjectStat]
    weak_topics: List[TopicStat]


class RecommendOut(BaseModel):
    topic_id: Optional[int] = None
    topic: Optional[str] = None
    message: str


class TutorIn(BaseModel):
    question: str = Field(min_length=1, max_length=300)


class TutorOut(BaseModel):
    answer: str
