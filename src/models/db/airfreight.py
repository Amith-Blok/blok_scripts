from pydantic import BaseModel
from typing import List, Literal

class Airline(BaseModel):
    code: Literal["QA", "EK"]
    name: Literal["Qatar Airways", "Emirates"]
    value: float
    currency: Literal["USD","INR"]
    transit_time: int

class Airfreight(BaseModel):
    start_code: str
    end_code: str
    airlines: List[Airline]