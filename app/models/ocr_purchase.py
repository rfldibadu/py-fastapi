from pydantic import BaseModel

class OCRRequest(BaseModel):
    uri: str
