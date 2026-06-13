from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.auth.dependencies import get_current_user

from app.models.user import User

from app.schemas.habit import (
    HabitCreate,
    HabitResponse,
    HabitToggleResponse,
    TodayHabitResponse,
    HabitAnalyticsResponse,
    MonthSheetResponse,
    HeatmapResponse,
    OverallAnalyticsResponse,
    MonthlyReportItem,
    MonthlyReportResponse,
    YearlyReportResponse,
    HabitUpdate,
    MessageResponse
)

from app.services.habit_service import (
    create_habit,
    get_user_habits,
    toggle_habit,
    get_today_habits,
    get_habit_analytics,
    get_month_sheet,
    get_heatmap_data,
    get_overall_analytics,
    get_monthly_reports,
    get_monthly_report_detail,
    get_yearly_report,
    update_habit,
    delete_habit
)

router = APIRouter(
    prefix="/habits",
    tags=["Habits"]
)

@router.post(
    "",
    response_model=HabitResponse
)
def add_habit(
    habit: HabitCreate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    return create_habit(
        db,
        user_id=user_id, #type:ignore
        title=habit.title
    )

@router.get("",response_model=list[HabitResponse])
def get_habits(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    return get_user_habits(db, user_id) #type:ignore

@router.post("/{habit_id}/toggle",response_model=HabitToggleResponse)
def toggle_habit_endpoint(
    habit_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    return toggle_habit(
        db,
        habit_id,
        current_user.id #type:ignore
    ) 

@router.get("/today",response_model=list[TodayHabitResponse])
def today_habits(
    current_user:User=Depends(get_current_user),
    db:Session=Depends(get_db)
):
    return get_today_habits(
        db,
        current_user.id #type:ignore
    )

@router.get(
    "/analytics/habit/{habit_id}",
    response_model=HabitAnalyticsResponse
)
def habit_analytics(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_habit_analytics(
        db,
        habit_id,
        current_user.id #type:ignore
    )


@router.get(
    "/month-sheet",
    response_model=list[MonthSheetResponse]
)
def month_sheet(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_month_sheet(
        db,
        current_user.id #type:ignore
    )

@router.get(
    "/analytics/heatmap",
    response_model=list[HeatmapResponse]
)
def heatmap(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_heatmap_data(
        db,
        current_user.id #type:ignore
    )

@router.get(
    "/analytics/overall",
    response_model=OverallAnalyticsResponse
)
def overall_analytics(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    return get_overall_analytics(
        db,
        current_user.id #type:ignore
    )

@router.get(
    "/reports/monthly",
    response_model=list[MonthlyReportItem]
)
def monthly_reports(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    return get_monthly_reports(
        db,
        current_user.id #type:ignore
    )

@router.get(
    "/reports/monthly/{year}/{month}",
    response_model=MonthlyReportResponse
)
def monthly_report_detail(
    year: int,
    month: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    return get_monthly_report_detail(
        db,
        current_user.id,
        year,
        month
    )

@router.get(
    "/reports/yearly",
    response_model=YearlyReportResponse
)
def yearly_report(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    return get_yearly_report(
        db,
        current_user.id #type: ignore
    )

@router.put(
    "/{habit_id}",
    response_model=HabitResponse
)
def edit_habit(
    habit_id: int,
    habit_data: HabitUpdate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    return update_habit(
        db,
        habit_id,
        current_user.id,
        habit_data.title
    )

def delete_habit(
    db: Session,
    habit_id: int,
    user_id: int
):

    habit = (
        db.query(Habit)
        .filter(
            Habit.id == habit_id,
            Habit.user_id == user_id,
            Habit.is_active == True
        )
        .first()
    )

    if not habit:
        return None

    habit.is_active = False

    db.commit()

    return {
        "message": "Habit deleted successfully"
    }

