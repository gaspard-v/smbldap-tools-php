from dataclasses import dataclass

@dataclass
class ErrorType:
    error_type: str
    error_message: str

@dataclass
class ErrorResponse:
    status_code: int
    error: ErrorType
    