import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool

from app.main import app as real_app
from app.db import get_session
from app.models.task import Task  # ensure model is registered

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

def override_get_session():
    with Session(test_engine) as session:
        yield session

@pytest.fixture(autouse=True)
def setup_db():
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)

@pytest.mark.asyncio
async def test_tasks_crud():
    test_app: FastAPI = real_app
    test_app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as ac:
        r = await ac.post("/tasks/", json={"title": "Read paper"})
        assert r.status_code == 201
        tid = r.json()["id"]

        r = await ac.get("/tasks/")
        assert any(t["id"] == tid for t in r.json())

        r = await ac.patch(f"/tasks/{tid}", json={"done": True})
        assert r.status_code == 200
        assert r.json()["done"] is True

        r = await ac.delete(f"/tasks/{tid}")
        assert r.status_code == 204
