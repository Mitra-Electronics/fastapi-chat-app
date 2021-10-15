from fastapi.exceptions import HTTPException

class RecoveryEmailError(HTTPException):
    """Custom error raised when Email and recovery email are the same"""

    def __init__(self,status: int, message: str) -> None:
        super().__init__(status,message)