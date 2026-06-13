from sqlalchemy.orm import Session
from app.models.habit import Habit
from app.models.habit_log import HabitLog
import calendar
from datetime import date,datetime,timedelta
from sqlalchemy import extract

def create_habit(
        db:Session,
        user_id: int,
        title: str
):
    habit=Habit(
        title=title,
        user_id=user_id    
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit

def get_user_habits(
        db:Session,
        user_id:int
):
    return(
        db.query(Habit)
        .filter(Habit.user_id==user_id,Habit.is_active==True)
        .all()
    )

def toggle_habit(
        db:Session,
        habit_id:int,
        user_id:int
):
    today =date.today()

    habit_log=(
        db.query(HabitLog).filter(
            HabitLog.habit_id==habit_id,
            HabitLog.user_id==user_id,
            HabitLog.date==today,
        ).first())

    if habit_log:
        habit_log.completed= not habit_log.completed
    else:
        habit_log=HabitLog(
            habit_id=habit_id,
            user_id=user_id,
            date=today,
            completed=True
        )
        db.add(habit_log)
    db.commit()
    db.refresh(habit_log)
    return habit_log

def get_today_habits(
        db:Session,
        user_id:int
):
    habits=(
        db.query(Habit).filter(
            Habit.user_id==user_id,
            Habit.is_active==True
        ).all()
    )

    today=date.today()
    result=[]
    for habit in habits:
        habit_log=(
            db.query(HabitLog).filter(
                HabitLog.habit_id == habit.id,
                HabitLog.user_id == user_id,
                HabitLog.date == today
            ).first()
        )
    result.append(
        {
            "habit_id": habit.id,
            "title": habit.title,
            "completed": (
                habit_log.completed
                if habit_log
                else False
            )
        }
    )
    return result

def get_habit_analytics(
    db: Session,
    habit_id: int,
    user_id: int
):

    habit = (
        db.query(Habit)
        .filter(
            Habit.id == habit_id,
            Habit.user_id == user_id
        )
        .first()
    )

    if not habit:
        return None

    completed_days = (
        db.query(HabitLog)
        .filter(
            HabitLog.habit_id == habit_id,
            HabitLog.user_id == user_id,
            HabitLog.completed == True
        )
        .count()
    )

    tracked_days = (
        datetime.utcnow().date()
        - habit.created_at.date()
    ).days + 1

    missed_days = tracked_days - completed_days

    completion_rate = (
        completed_days / tracked_days * 100
    ) if tracked_days > 0 else 0

    return {
        "habit": habit.title,
        "tracked_days": tracked_days,
        "completed_days": completed_days,
        "missed_days": missed_days,
        "completion_rate": round(completion_rate, 2)
    }

def get_month_sheet(
    db: Session,
    user_id: int
):

    habits = (
        db.query(Habit)
        .filter(
            Habit.user_id == user_id,
            Habit.is_active == True
        )
        .all()
    )

    today = date.today()

    current_month = today.month
    current_year = today.year

    days_in_month = calendar.monthrange(
        current_year,
        current_month
    )[1]

    result = []

    for habit in habits:

        day_map = {
            day: False
            for day in range(
                1,
                days_in_month + 1
            )
        }

        logs = (
            db.query(HabitLog)
            .filter(
                HabitLog.habit_id == habit.id,
                HabitLog.user_id == user_id
            )
            .all()
        )

        for log in logs:

            if (
                log.date.month == current_month
                and
                log.date.year == current_year
            ):

                day_map[
                    log.date.day
                ] = log.completed

        result.append(
            {
                "habit_id": habit.id,
                "title": habit.title,
                "days": day_map
            }
        )

    return result

def get_heatmap_data(
    db: Session,
    user_id: int
):

    habits = (
        db.query(Habit)
        .filter(
            Habit.user_id == user_id,
            Habit.is_active == True
        )
        .all()
    )

    if not habits:
        return []

    start_date = min(
        habit.created_at.date()
        for habit in habits
    )

    end_date = date.today()

    result = []

    current_day = start_date

    while current_day <= end_date:

        active_habits = [
            habit
            for habit in habits
            if habit.created_at.date() <= current_day
        ]

        total_habits = len(active_habits)

        completed_count = (
            db.query(HabitLog)
            .filter(
                HabitLog.user_id == user_id,
                HabitLog.date == current_day,
                HabitLog.completed == True
            )
            .count()
        )

        score = (
            completed_count / total_habits * 100
            if total_habits > 0
            else 0
        )

        result.append(
            {
                "date": current_day,
                "score": round(score, 2)
            }
        )

        current_day += timedelta(days=1)

    return result

def get_overall_analytics(
    db: Session,
    user_id: int
):

    habits = (
        db.query(Habit)
        .filter(
            Habit.user_id == user_id,
            Habit.is_active == True
        )
        .all()
    )

    total_habits = len(habits)

    if total_habits == 0:
        return {
            "discipline_score": 0,
            "total_habits": 0,
            "total_completed": 0,
            "total_possible": 0,
            "best_habit": None,
            "worst_habit": None
        }

    total_completed = 0
    total_possible = 0

    habit_scores = []

    today = datetime.utcnow().date()

    for habit in habits:

        tracked_days = (
            today
            - habit.created_at.date()
        ).days + 1

        completed_days = (
            db.query(HabitLog)
            .filter(
                HabitLog.habit_id == habit.id,
                HabitLog.user_id == user_id,
                HabitLog.completed == True
            )
            .count()
        )

        total_completed += completed_days
        total_possible += tracked_days

        completion_rate = (
            completed_days
            / tracked_days
            * 100
        ) if tracked_days > 0 else 0

        habit_scores.append(
            (
                habit.title,
                completion_rate
            )
        )

    discipline_score = (
        total_completed
        / total_possible
        * 100
    ) if total_possible > 0 else 0

    best_habit = max(
        habit_scores,
        key=lambda x: x[1]
    )[0]

    worst_habit = min(
        habit_scores,
        key=lambda x: x[1]
    )[0]

    return {
        "discipline_score": round(
            discipline_score,
            2
        ),
        "total_habits": total_habits,
        "total_completed": total_completed,
        "total_possible": total_possible,
        "best_habit": best_habit,
        "worst_habit": worst_habit
    }

def get_monthly_reports(
    db: Session,
    user_id: int
):
    report = get_monthly_reports(
        db,
        user_id
    )

    return [
        {
            "month": report["month"],
            "discipline_score": report["discipline_score"]
        }
    ]

def get_monthly_report_detail(
    db: Session,
    user_id: int,
    year: int,
    month: int
):

    habits = (
        db.query(Habit)
        .filter(
            Habit.user_id == user_id,
            Habit.is_active == True
        )
        .all()
    )

    total_completed = 0
    total_possible = 0

    habit_scores = []

    report_start = date(
        year,
        month,
        1
    )

    today = date.today()

    for habit in habits:

        if habit.created_at.date() > today:
            continue

        habit_start = max(
            habit.created_at.date(),
            report_start
        )

        if year == today.year and month == today.month:

            report_end = today

        else:

            import calendar

            last_day = calendar.monthrange(
                year,
                month
            )[1]

            report_end = date(
                year,
                month,
                last_day
            )

        tracked_days = (
            report_end - habit_start
        ).days + 1

        if tracked_days <= 0:
            continue

        completed_days = (
            db.query(HabitLog)
            .filter(
                HabitLog.habit_id == habit.id,
                HabitLog.user_id == user_id,
                HabitLog.completed == True
            )
            .filter(
                extract(
                    "month",
                    HabitLog.date
                ) == month
            )
            .filter(
                extract(
                    "year",
                    HabitLog.date
                ) == year
            )
            .count()
        )

        total_completed += completed_days
        total_possible += tracked_days

        completion_rate = (
            completed_days
            / tracked_days
            * 100
        )

        habit_scores.append(
            (
                habit.title,
                completion_rate
            )
        )

    discipline_score = (
        total_completed
        / total_possible
        * 100
    ) if total_possible > 0 else 0

    best_habit = (
        max(
            habit_scores,
            key=lambda x: x[1]
        )[0]
        if habit_scores
        else None
    )

    worst_habit = (
        min(
            habit_scores,
            key=lambda x: x[1]
        )[0]
        if habit_scores
        else None
    )

    return {
        "month": report_start.strftime(
            "%B %Y"
        ),
        "discipline_score": round(
            discipline_score,
            2
        ),
        "total_completed": total_completed,
        "total_possible": total_possible,
        "best_habit": best_habit,
        "worst_habit": worst_habit
    }

def get_yearly_report(
    db: Session,
    user_id: int
):

    current_year = date.today().year

    habits = (
        db.query(Habit)
        .filter(
            Habit.user_id == user_id,
            Habit.is_active == True
        )
        .all()
    )

    total_completed = 0
    total_possible = 0

    habit_scores = []

    month_scores = []

    for month in range(1, 13):

        month_completed = 0
        month_possible = 0

        report_start = date(
            current_year,
            month,
            1
        )

        last_day = calendar.monthrange(
            current_year,
            month
        )[1]

        report_end = date(
            current_year,
            month,
            last_day
        )

        if report_end > date.today():
            report_end = date.today()

        for habit in habits:

            habit_start = max(
                habit.created_at.date(),
                report_start
            )

            tracked_days = (
                report_end - habit_start
            ).days + 1

            if tracked_days <= 0:
                continue

            completed_days = (
                db.query(HabitLog)
                .filter(
                    HabitLog.habit_id == habit.id,
                    HabitLog.user_id == user_id,
                    HabitLog.completed == True
                )
                .filter(
                    extract(
                        "month",
                        HabitLog.date
                    ) == month
                )
                .filter(
                    extract(
                        "year",
                        HabitLog.date
                    ) == current_year
                )
                .count()
            )

            month_completed += completed_days
            month_possible += tracked_days

            total_completed += completed_days
            total_possible += tracked_days

        month_score = (
            month_completed
            / month_possible
            * 100
        ) if month_possible > 0 else 0

        month_scores.append(
            (
                calendar.month_name[month],
                round(month_score, 2)
            )
        )

    for habit in habits:

        tracked_days = (
            date.today()
            - habit.created_at.date()
        ).days + 1

        completed_days = (
            db.query(HabitLog)
            .filter(
                HabitLog.habit_id == habit.id,
                HabitLog.user_id == user_id,
                HabitLog.completed == True
            )
            .filter(
                extract(
                    "year",
                    HabitLog.date
                ) == current_year
            )
            .count()
        )

        completion_rate = (
            completed_days
            / tracked_days
            * 100
        ) if tracked_days > 0 else 0

        habit_scores.append(
            (
                habit.title,
                completion_rate
            )
        )

    discipline_score = (
        total_completed
        / total_possible
        * 100
    ) if total_possible > 0 else 0

    best_habit = (
        max(
            habit_scores,
            key=lambda x: x[1]
        )[0]
        if habit_scores
        else None
    )

    worst_habit = (
        min(
            habit_scores,
            key=lambda x: x[1]
        )[0]
        if habit_scores
        else None
    )

    best_month = (
        max(
            month_scores,
            key=lambda x: x[1]
        )[0]
        if month_scores
        else None
    )

    worst_month = (
        min(
            month_scores,
            key=lambda x: x[1]
        )[0]
        if month_scores
        else None
    )

    return {
        "year": current_year,
        "discipline_score": round(
            discipline_score,
            2
        ),
        "total_completed": total_completed,
        "total_possible": total_possible,
        "best_habit": best_habit,
        "worst_habit": worst_habit,
        "best_month": best_month,
        "worst_month": worst_month
    }

def update_habit(
    db: Session,
    habit_id: int,
    user_id: int,
    title: str
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

    habit.title = title

    db.commit()
    db.refresh(habit)

    return habit

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