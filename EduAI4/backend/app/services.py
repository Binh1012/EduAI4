"""Learning analytics. Rule-based now; swap these functions for an ML model later
(same inputs/outputs) without touching the routers or the Android app."""
from datetime import timedelta
from typing import Dict

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from .config import settings
from .models import Question, QuizResult, Subject, Topic, UserAnswer, now


def topic_stats(db: Session, user_id: int) -> Dict[int, dict]:
    rows = (
        db.query(Topic.id, Topic.name, Subject.name, func.count(UserAnswer.id),
                 func.sum(case((UserAnswer.is_correct.is_(True), 1), else_=0)))
        .join(Subject, Subject.id == Topic.subject_id)
        .join(Question, Question.topic_id == Topic.id)
        .join(UserAnswer, UserAnswer.question_id == Question.id)
        .join(QuizResult, QuizResult.id == UserAnswer.result_id)
        .filter(QuizResult.user_id == user_id)
        .group_by(Topic.id, Topic.name, Subject.name)
        .all()
    )
    return {
        tid: {"topic_id": tid, "topic": tn, "subject": sn, "total": total,
              "correct": int(correct or 0), "accuracy": round(100 * int(correct or 0) / total)}
        for tid, tn, sn, total, correct in rows
    }


def weak_topics(stats: Dict[int, dict]):
    weak = [s for s in stats.values() if s["total"] >= 3 and s["accuracy"] < settings.WEAK_THRESHOLD]
    return sorted(weak, key=lambda s: s["accuracy"])


def streak_days(db: Session, user_id: int) -> int:
    days = {d.date() for (d,) in db.query(QuizResult.created_at).filter(QuizResult.user_id == user_id)}
    day = now().date()
    if day not in days:
        day -= timedelta(days=1)
    n = 0
    while day in days:
        n += 1
        day -= timedelta(days=1)
    return n


def recommend(db: Session, user_id: int) -> dict:
    stats = topic_stats(db, user_id)
    weak = weak_topics(stats)
    if weak:
        w = weak[0]
        return {"topic_id": w["topic_id"], "topic": w["topic"],
                "message": f"Bạn nên ôn lại “{w['topic']}” (đúng {w['accuracy']}%)."}
    for t in db.query(Topic).order_by(Topic.id):
        if t.id not in stats:
            return {"topic_id": t.id, "topic": t.name, "message": f"Thử chủ đề mới: “{t.name}”."}
    return {"topic_id": None, "topic": None, "message": "Em học rất tốt! Hãy luyện thêm để giỏi hơn nhé."}
