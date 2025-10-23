from sqlalchemy.orm import Session
from . import models, schemas

# ----------------------
# ✅ Create Task
# ----------------------
def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        title=task.title,
        description=task.description or "",
        status=task.status or "Pending",
        priority=task.priority or "Medium",
        due_date=task.due_date,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# ----------------------
# ✅ Get All Tasks
# ----------------------
def get_tasks(db: Session):
    return db.query(models.Task).all()


# ----------------------
# ✅ Get Task by ID
# ----------------------
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id.__eq__(task_id)).first()


# ----------------------
# ✅ Update Task
# ----------------------
def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.id.__eq__(task_id)).first()
    if db_task is None:
        return None

    # Use Pydantic v2's model_dump to get updated fields
    update_data = task.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


# ----------------------
# ✅ Delete Task
# ----------------------
def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id.__eq__(task_id)).first()
    if db_task is None:
        return None

    db.delete(db_task)
    db.commit()
    return db_task
