import json
from pathlib import Path

from .models import Question, Subject, Topic


def seed(db):
    """Load sample data once (only when the database is empty)."""
    if db.query(Subject).count():
        return
    data = json.loads(Path(__file__).with_name("seed_data.json").read_text(encoding="utf-8"))
    for s in data:
        subject = Subject(name=s["name"], icon=s["icon"], color=s["color"])
        for t in s["topics"]:
            topic = Topic(name=t["name"])
            topic.questions = [Question(**q) for q in t["questions"]]
            subject.topics.append(topic)
        db.add(subject)
    db.commit()
