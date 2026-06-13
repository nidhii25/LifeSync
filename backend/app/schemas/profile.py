from pydantic import BaseModel
from typing import Optional

class ProfileCreate(BaseModel):

    age: int

    gender: str

    height_cm: float

    current_weight: float

    target_weight: float

    occupation: str

    bio: str

class ProfileUpdate(BaseModel):

    age: Optional[int] = None

    gender: Optional[str] = None

    height_cm: Optional[float] = None

    current_weight: Optional[float] = None

    target_weight: Optional[float] = None

    occupation: Optional[str] = None

    bio: Optional[str] = None

class ProfileResponse(BaseModel):

    id: int

    user_id: int

    age: int

    gender: str

    height_cm: float

    current_weight: float

    target_weight: float

    occupation: str

    bio: str

    class Config:

        from_attributes = True