from sqlalchemy.orm import Session

from app.models.profile import Profile

from app.schemas.profile import (
    ProfileCreate,
    ProfileUpdate
)

def create_profile(
    db: Session,
    user_id: int,
    profile_data: ProfileCreate
):

    existing_profile = (
        db.query(Profile)
        .filter(Profile.user_id == user_id)
        .first()
    )

    if existing_profile:
        return existing_profile

    profile = Profile(
        user_id=user_id,
        age=profile_data.age,
        gender=profile_data.gender,
        height_cm=profile_data.height_cm,
        current_weight=profile_data.current_weight,
        target_weight=profile_data.target_weight,
        occupation=profile_data.occupation,
        bio=profile_data.bio
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile

def get_profile(
    db: Session,
    user_id: int
):

    return (
        db.query(Profile)
        .filter(Profile.user_id == user_id)
        .first()
    )

def update_profile(
    db: Session,
    user_id: int,
    profile_data: ProfileUpdate
):

    profile = (
        db.query(Profile)
        .filter(Profile.user_id == user_id)
        .first()
    )

    if not profile:
        return None

    update_data = profile_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():

        setattr(
            profile,
            field,
            value
        )

    db.commit()
    db.refresh(profile)

    return profile