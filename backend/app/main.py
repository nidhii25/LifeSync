from fastapi import FastAPI
from app.database.database import Base, engine

from app.models.user import User
from app.models.habit import Habit
from app.models.profile import Profile
from app.models.habit_log import HabitLog
from app.auth.auth_router import router as auth_router
from app.api.habit_router import router as habit_router
from app.api.profile_router import router as profile_router

app = FastAPI(
    title="LifeSync API"
)

app.include_router(auth_router)
app.include_router(habit_router)
app.include_router(profile_router)
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "message": "LifeSync Backend Running"
    }