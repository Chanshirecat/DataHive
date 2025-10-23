from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import database, models
import plotly.express as px
import pandas as pd
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/tasks_by_status_chart", response_class=HTMLResponse)
def tasks_by_status_chart(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    if not tasks:
        return "<h3>No tasks found</h3>"

    # Convert tasks to DataFrame
    df = pd.DataFrame([{
        "status": t.status,
        "priority": t.priority,
        "title": t.title
    } for t in tasks])

    fig = px.bar(
        df.groupby("status").size().reset_index(name="count"),
        x="status",
        y="count",
        title="Tasks by Status",
        color="status"
    )

    # Return HTML div
    return fig.to_html(full_html=False)
