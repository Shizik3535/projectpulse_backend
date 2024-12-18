from fastapi import status, HTTPException


class ManagerService:
    @classmethod
    def _check_role(cls, role: str):
        if role != "Менеджер":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав"
            )
