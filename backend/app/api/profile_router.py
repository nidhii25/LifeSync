from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.auth.dependencies import get_current_user

from app.models.user import User

from app.schemas.profile import (
    ProfileCreate,
    ProfileUpdate,
    ProfileResponse
)

from app.services.profile_service import (
    create_profile,
    get_profile,
    update_profile
)

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)

@router.post(
    "",
    response_model=ProfileResponse
)
def create_user_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    return create_profile(
        db,
        current_user.id,  # type: ignore
        profile_data
    )

@router.get(
    "",
    response_model=ProfileResponse
)
def get_user_profile(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    profile = get_profile(
        db,
        current_user.id  # type: ignore
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile

@router.put(
    "",
    response_model=ProfileResponse
)
def update_user_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    profile = update_profile(
        db,
        current_user.id,  # type: ignore
        profile_data
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile