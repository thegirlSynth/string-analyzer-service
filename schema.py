from pydantic import BaseModel

class StringInput(BaseModel):
    value: str
