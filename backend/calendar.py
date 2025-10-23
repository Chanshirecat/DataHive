from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import null
from . import database, models
import plotly.express as px
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/calendar", tags=["calendar"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/tasks_due", response_class=HTMLResponse)
def tasks_due_calendar(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.due_date.isnot(None)).all()
    if not tasks:
        return "<h3>There are no tasks with due dates</h3>"

    data = [{
        "Task": t.title,
        "Start": t.due_date,
        "End": t.due_date
    } for t in tasks]

    fig = px.timeline(data, x_start="Start", x_end="End", y="Task", title="Tasks Due Calendar")
    fig.update_yaxes(autorange="reversed")  # Show earliest tasks at top
    return fig.to_html(full_html=False)
