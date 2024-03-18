from dataclasses import dataclass

@dataclass
class ErrorType:
    error_type: str
    error_message: str

@dataclass
class ErrorResponse:
    status_code: int
    error: ErrorType
    
def build_error_response(
    status_code: int,
    error_type: str,
    error_message: str
) -> ErrorResponse:
    return ErrorResponse(
            status_code,
            ErrorType(
                error_type,
                error_message
            )
        )
    