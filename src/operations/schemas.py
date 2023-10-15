from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Operation(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str

    class Config:
        from_attributes = True


class OperationResponse(BaseModel):
    status: str
    data: List[Operation]
    details: Optional[str]
