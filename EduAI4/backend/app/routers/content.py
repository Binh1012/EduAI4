from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import current_user
from ..models import Question, Subject, Topic, User
from ..schemas import QuestionOut, SubjectOut, TopicOut
from ..services import topic_stats

router = APIRouter(tags=["content"])


@router.get("/subjects", response_model=List[SubjectOut])
def subjects(user: User = Depends(current_user), db: Session = Depends(get_db)):
    stats = topic_stats(db, user.id)
    return [
        SubjectOut(id=s.id, name=s.name, icon=s.icon, color=s.color,
                   topics=[TopicOut(id=t.id, name=t.name, accuracy=stats.get(t.id, {}).get("accuracy"))
                           for t in s.topics])
        for s in db.query(Subject).order_by(Subject.id)
    ]


@router.get("/topics/{topic_id}/questions", response_model=List[QuestionOut])
def questions(topic_id: int, limit: int = Query(10, ge=1, le=50),
              user: User = Depends(current_user), db: Session = Depends(get_db)):
    if not db.get(Topic, topic_id):
        raise HTTPException(404, "Không tìm thấy chủ đề")
    rows = db.query(Question).filter(Question.topic_id == topic_id).order_by(func.random()).limit(limit).all()
    # Practice mode: the app shows instant feedback, so the answer is included.
    # The server re-grades on submit, so scores cannot be faked.
    return [QuestionOut(id=q.id, text=q.text, options=q.options, correct_index=q.correct_index,
                        explanation=q.explanation or "") for q in rows]
