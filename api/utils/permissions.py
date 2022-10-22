from fastapi import HTTPException, status

from db.models.user import User


def verify_role(required_role: list, user: User):
    if user.role.value not in required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
