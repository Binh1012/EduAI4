from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import current_user
from ..models import Question, QuizResult, Subject, Topic, User, UserAnswer
from ..schemas import ProgressOut, RecommendOut, ResultOut, SubjectStat, SubmitIn, TopicStat
from ..services import recommend, streak_days, topic_stats, weak_topics

router = APIRouter(tags=["learning"])


@router.post("/quiz/submit", response_model=ResultOut)
def submit(body: SubmitIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if not db.get(Topic, body.topic_id):
        raise HTTPException(404, "Không tìm thấy chủ đề")
    picked = {a.question_id: a.selected for a in body.answers}  # de-duplicate
    questions = db.query(Question).filter(Question.id.in_(picked), Question.topic_id == body.topic_id).all()
    if not questions:
        raise HTTPException(400, "Bài làm không hợp lệ")
    graded = [(q, picked[q.id], picked[q.id] == q.correct_index) for q in questions]
    correct = sum(1 for _, _, ok in graded if ok)
    total = len(graded)
    xp = correct * 10 + (20 if correct == total else 0)
    result = QuizResult(user_id=user.id, topic_id=body.topic_id, correct=correct, total=total, xp=xp)
    db.add(result)
    db.flush()
    db.add_all([UserAnswer(result_id=result.id, question_id=q.id, selected=sel, is_correct=ok)
                for q, sel, ok in graded])
    db.commit()
    return ResultOut(correct=correct, total=total, percent=round(100 * correct / total), xp_gained=xp)


@router.get("/progress", response_model=ProgressOut)
def progress(user: User = Depends(current_user), db: Session = Depends(get_db)):
    stats = topic_stats(db, user.id)
    per_subject = {}
    for s in stats.values():
        c, t = per_subject.get(s["subject"], (0, 0))
        per_subject[s["subject"]] = (c + s["correct"], t + s["total"])
    xp, done = db.query(func.coalesce(func.sum(QuizResult.xp), 0), func.count(QuizResult.id)) \
        .filter(QuizResult.user_id == user.id).one()
    perfect = db.query(func.count(QuizResult.id)).filter(
        QuizResult.user_id == user.id, QuizResult.correct == QuizResult.total).scalar()
    return ProgressOut(
        xp=int(xp), level=int(xp) // 100 + 1, streak=streak_days(db, user.id),
        quizzes_done=done, perfect_quizzes=perfect,
        subjects=[SubjectStat(subject=s.name,
                              accuracy=round(100 * per_subject[s.name][0] / per_subject[s.name][1])
                              if s.name in per_subject else None)
                  for s in db.query(Subject).order_by(Subject.id)],
        weak_topics=[TopicStat(**{k: w[k] for k in ("topic_id", "topic", "subject", "accuracy", "total")})
                     for w in weak_topics(stats)],
    )


@router.get("/recommendations", response_model=RecommendOut)
def recommendations(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return recommend(db, user.id)
