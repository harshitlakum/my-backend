from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import init_db
from app.routers.tasks import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    init_db()
    yield
    # shutdown (nothing yet)

app = FastAPI(title="My Backend (Local)", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(tasks_router)
