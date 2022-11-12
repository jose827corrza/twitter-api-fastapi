from pydantic import BaseModel

from fastapi.responses import JSONResponse
# from main import app

class Error(BaseModel):
    statusCode: int
    errorDescription: str