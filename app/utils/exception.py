# utils/exception.py

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class PurchaseValidationError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

def purchase_validation_exception_handler(request: Request, exc: PurchaseValidationError):
    return JSONResponse(
        status_code=422,
        content={"message": f"Purchase validation failed: {exc.detail}"}
    )
