from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session

from app.db import get_session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskRead, status_code=201)
def create_task(payload: TaskCreate, session: Session = Depends(get_session)):
    task = Task(title=payload.title)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/", response_model=List[TaskRead])
def list_tasks(
    session: Session = Depends(get_session),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    res = session.exec(select(Task).offset(offset).limit(limit))
    return res.all()

@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(task, k, v)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(task)
    session.commit()
    return None
