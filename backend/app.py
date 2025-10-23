from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from . import crud, database, calendar
from .analytics import router as analytics_router
from pydantic import BaseModel

# -------------------------------------------------
# Create FastAPI instance
# -------------------------------------------------
app = FastAPI(title="DataHive Task Tracker")

# Include routers for other modules
app.include_router(analytics_router)
app.include_router(calendar.router)


# -------------------------------------------------
# Pydantic models for creating and updating tasks
# -------------------------------------------------
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "Pending"
    priority: Optional[str] = "Medium"
    due_date: Optional[datetime] = None

    class Config:
        from_attributes = True  # ✅ Pydantic v2


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None

    class Config:
        from_attributes = True


# -------------------------------------------------
# Dependency to get DB session
# -------------------------------------------------
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------
# CRUD Endpoints
# -------------------------------------------------
@app.post("/tasks/", response_model=dict)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)


@app.get("/tasks/", response_model=List[dict])
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)


@app.get("/tasks/{task_id}", response_model=dict)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.put("/tasks/{task_id}", response_model=dict)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True}
