from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models  # noqa: F401  (register tables)
from .database import Base, SessionLocal, engine
from .routers import ai, auth, content, learning
from .seed import seed


@asynccontextmanager
async def lifespan(_):
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        seed(db)
    yield


app = FastAPI(title="EduAI 4 API", version="1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])  # tighten in production
for r in (auth.router, content.router, learning.router, ai.router):
    app.include_router(r)


@app.get("/health")
def health():
    return {"status": "ok"}
