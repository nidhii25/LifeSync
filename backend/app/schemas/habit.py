from pydantic import BaseModel
from datetime import date

class HabitCreate(BaseModel):
    title:str

class HabitResponse(BaseModel):
    id:int
    title:str
    is_active:bool
    
    class Config:
        from_attributes = True

class HabitLogResponse(BaseModel):
    habit_id:int
    title:int
    date:date
    completed:bool

class HabitToggleResponse(BaseModel):
    habit_id: int
    completed: bool
    date: date

    class Config:
        from_attributes = True

class TodayHabitResponse(BaseModel):
    habit_id:int
    title:str
    completed:bool

class HabitAnalyticsResponse(BaseModel):
    habit:str
    tracked_days: int
    completed_days: int
    missed_days: int
    completion_rate: float

class MonthSheetResponse(BaseModel):
    habit_id:int
    title:str
    days:dict[int,bool]

class HeatmapResponse(BaseModel):
    date:date
    score:float

class OverallAnalyticsResponse(BaseModel):
    discipline_score: float
    total_habits: int
    total_completed: int
    total_possible: int
    best_habit: str | None
    worst_habit: str | None

class MonthlyReportResponse(BaseModel):
    month: str
    discipline_score: float
    total_completed: int
    total_possible: int
    best_habit: str | None
    worst_habit: str | None

class MonthlyReportItem(BaseModel):
    month: str
    discipline_score: float

class YearlyReportResponse(BaseModel):
    year: int
    discipline_score: float
    total_completed: int
    total_possible: int
    best_habit: str | None
    worst_habit: str | None
    best_month: str | None
    worst_month: str | None

class HabitUpdate(BaseModel):
    title: str

class MessageResponse(BaseModel):
    message: str